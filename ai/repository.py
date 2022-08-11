from datetime import datetime
from typing import Optional, List

import requests
from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder

import ai.schema as AISchema
from config import settings
from database import MotorDB

motor = MotorDB()


async def get_movie(movie_id: Optional[str] = None, title: Optional[str] = None):
    await motor.connect_db(db_name="movie_predictor")
    movie_col = await motor.get_collection(col_name="movie")
    movie = None

    if movie_id is not None:
        movie = await movie_col.find_one({"movieId": movie_id})
        if movie is not None:
            api_url = settings.TMDB_URL + "movie/" + movie["tmdbId"] + "?api_key=" + settings.TMDB_API_KEY
            response = requests.get(api_url)
            movie.update({
                "movieDetails": response.json()
            })
            return movie

    if title is not None:
        movie = await movie_col.find_one({"title": title})
        if movie is not None:
            return movie

    return None


async def add_movie(movie: AISchema.Movie):
    await motor.connect_db(db_name="movie_predictor")
    movie_col = await motor.get_collection(col_name="movie")

    movie_exist = await get_movie(movie_id=movie['movieId'], title=movie['title'])

    if movie_col is not None and movie_exist is None:
        new_movie = await movie_col.insert_one(movie)
        if not new_movie:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Movie creation failed"
            )
        else:
            created_movie = await movie_col.find_one({"_id": new_movie.inserted_id})

            return created_movie

    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Movie Already Exists"
        )


async def get_rating(movie_id: str, user_id: str):
    await motor.connect_db(db_name="movie_predictor")
    rating_col = await motor.get_collection(col_name="rating")
    rating_exist = None

    if rating_col is not None:
        rating_exist = await rating_col.find_one({
            "$and": [
                {"movieId": movie_id},
                {"userId": user_id}
            ]
        })
        if rating_exist is None:
            rating_exist = {
                "movieId": movie_id,
                "userId": user_id,
                "rating": 0
            }

    return rating_exist


async def get_users_rating_all(user_id: str):
    await motor.connect_db(db_name="movie_predictor")
    rating_col = await motor.get_collection(col_name="rating")
    if rating_col is not None:
        rating_count = await rating_col.count_documents({"userId": user_id})
        return rating_count


async def add_user_preferences(user_id: str, preferences: List[str]):
    await motor.connect_db(db_name="movie_predictor")
    preferences_col = await motor.get_collection(col_name="preferences")

    existing_pref = await preferences_col.find_one({"userId": user_id})
    if existing_pref is not None:
        if existing_pref["preferences"] == preferences:
            return existing_pref
        else:
            new_preference = {
                "userId": user_id,
                "preferences": preferences
            }
            result = await preferences_col.replace_one({"_id": existing_pref["_id"]}, new_preference)
            updated_preference = await preferences_col.find_one({"userId": user_id})
            return updated_preference
    else:
        if preferences_col is not None:
            # new_preference = {
            #     "userId": user_id,
            #     "preferences": preferences
            # }

            new_preference = AISchema.Preferences(userId=user_id, preferences=preferences)
            new_preference = jsonable_encoder(new_preference)
            result = await preferences_col.insert_one(new_preference)

            if not result:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Preference creation failed"
                )
            else:
                created_preference = await preferences_col.find_one({"userId": user_id})
                return created_preference


async def get_user_preferences(user_id: str):
    await motor.connect_db(db_name="movie_predictor")
    preferences_col = await motor.get_collection(col_name="preferences")
    preferences = await preferences_col.find_one({"userId": user_id})
    if not preferences:
        return {
            "preferences": []
        }
    else:
        return preferences


async def add_rating(rating: AISchema.Rating):
    await motor.connect_db(db_name="movie_predictor")
    rating_col = await motor.get_collection(col_name="rating")

    rating = jsonable_encoder(rating)

    if rating_col is not None:
        rating_exist = await get_rating(movie_id=rating["movieId"], user_id=rating["userId"])
        if rating_exist["rating"] == 0:
            new_rating = await rating_col.insert_one(rating)
            if not new_rating:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Rating creation failed"
                )
            else:
                created_rating = await rating_col.find_one({"_id": new_rating.inserted_id})
                return created_rating
        else:
            update_rating = {
                "userId": rating["userId"],
                "movieId": rating["movieId"],
                "rating": rating["rating"],
                "timestamp": datetime.now()
            }
            result = await rating_col.replace_one({"_id": rating_exist['_id']}, update_rating)
            updated_doc = await rating_col.find_one({"_id": rating_exist['_id']})
            return updated_doc


async def add_comments(comment: AISchema.Comment, movie_id: str):
    await motor.connect_db(db_name="movie_predictor")
    forum_col = await motor.get_collection(col_name="forum")

    movie_forum = await forum_col.find_one({"movieId": movie_id})
    if movie_forum is None:
        comment = dict(comment)
        new_comment = AISchema.Comment(userId=comment["userId"], comment=comment["comment"])

        comments = [new_comment.dict()]

        new_forum = AISchema.Forum(movieId=movie_id, comments=comments)
        new_forum = jsonable_encoder(new_forum)

        inserted_forum = await forum_col.insert_one(new_forum)

        if inserted_forum:
            await forum_col.find_one({"_id": inserted_forum.inserted_id})
            return {
                "movieId": movie_id,
                "new_comment": new_comment.dict()
            }
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unable to add comment")

    else:
        comments = movie_forum["comments"]
        comment = dict(comment)
        new_comment = AISchema.Comment(userId=comment["userId"], comment=comment["comment"])
        new_comment = new_comment.dict()

        updated_forum = await forum_col.update_one({"movieId": movie_id}, {"$push": {"comments": new_comment}})

        if updated_forum.modified_count > 0:
            return {
                "movieId": movie_id,
                "new_comment": new_comment
            }
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unable to add comment")


async def add_to_watchlist(user_id: str, movie_ids: List[str]):
    await motor.connect_db(db_name="movie_predictor")
    watchlist_col = await motor.get_collection(col_name="watchlists")

    result = await watchlist_col.replace_one({"userId": user_id}, {"movieIds": movie_ids, "userId": user_id},
                                             upsert=True)

    if result.modified_count > 0 or result.upserted_id:
        return {
            "movieIds": movie_ids,
            "userId": user_id,
            "status": "Updated"
        }


async def get_watchlist(user_id: str):
    await motor.connect_db(db_name="movie_predictor")
    watchlist_col = await motor.get_collection(col_name="watchlists")

    result = await watchlist_col.find_one({"userId": user_id})
    watchlist = []
    if result is not None:
        for movie_id in result["movieIds"]:
            watchlist.append(await get_movie(movie_id=movie_id))

    return watchlist


# AI Algorithms

async def to_df(list_of_docs):
    import pandas as pd
    df = pd.json_normalize(list_of_docs)
    df.drop(['_id'], axis=1, inplace=True)
    return df


async def get_all_rating():
    from surprise import Reader, Dataset
    from pandas import to_numeric

    await motor.connect_db(db_name="movie_predictor")
    rating_col = await motor.get_collection(col_name="rating")

    size = await rating_col.count_documents({})

    ratingset = []
    cursor = rating_col.find({})
    for doc in await cursor.to_list(size):
        ratingset.append(doc)
    df = await to_df(ratingset)
    cols = df.columns
    df[cols] = df[cols].apply(to_numeric, errors="coerce")

    reader = Reader(rating_scale=(1, 5))
    dataset = Dataset.load_from_df(df[["userId", "movieId", "rating"]], reader=reader)
    return (dataset)


async def load_model(model_filename):
    from surprise import dump
    import os
    file_name = os.path.expanduser(model_filename)
    _, loaded_model = dump.load(file_name)
    return loaded_model


async def movieid_to_name(movieID):
    await motor.connect_db(db_name="movie_predictor")
    movie_col = await motor.get_collection(col_name="movie")

    cursor = movie_col.find({"movieId": str(movieID)})
    for doc in await cursor.to_list(10):
        return doc


async def KNNBasicModel():
    from surprise import KNNBasic
    from surprise import dump

    dataset = await get_all_rating()
    trainset = dataset.build_full_trainset()
    dump.dump("./ai/models/trainset", algo=trainset)

    # computing similarity matrix with K Nearest Neighbour algorithm and cosine similarity
    # we are using item based collaborative filtering hence user_based should be false

    algo = KNNBasic(sim_options={
        'name': 'cosine',
        'user_based': False
    }).fit(trainset)

    similarity_matrix = algo.compute_similarities()
    dump.dump("./ai/models/KNNBasicModel", algo=similarity_matrix)


async def collab_recommend(user_id):
    import heapq
    from collections import defaultdict
    from operator import itemgetter

    trainset = await load_model("./ai/models/trainset")
    similarity_matrix = await load_model("./ai/models/KNNBasicModel")

    # calculating by using 20 nearest neighbors
    k = 20

    # finding the top 20 rated movies by user
    test_subject_IID = trainset.to_inner_uid(user_id)
    test_subject_ratings = trainset.ur[test_subject_IID]
    k_neighbours = heapq.nlargest(k, test_subject_ratings, key=lambda x: x[1])

    # will thrwo keyerror if we use a normal dictionary since we cannot search with a non-existent key in a normal dict
    # finding similarities of each element in k_neighbours and storing them by assigning each of them a score
    # to improvde the accuracy of the score modifying the default score as score*(rating/5.0)
    candidates = defaultdict(float)

    for itemID, rating in k_neighbours:
        similarities = similarity_matrix[itemID]
        for innerID, score in enumerate(similarities):
            candidates[innerID] += score * (rating / 5.0)

    watched = []
    for itemID, rating in trainset.ur[test_subject_IID]:
        watched.append(itemID)

    recommendation = []
    position = 0

    # candidates have a structure of innerid : score hence we need to sort candidates descending order of score
    for itemID, _ in sorted(candidates.items(), key=itemgetter(1), reverse=True):
        if not itemID in watched:
            recommendation.append(await movieid_to_name(trainset.to_raw_iid(itemID)))
            position += 1
            if (position > 10): break

    recommendation_response = []
    recommendation_ratings = []
    rating_counts = await get_users_rating_all(user_id=str(user_id))
    preferences = await get_user_preferences(user_id=str(user_id))

    for movie in recommendation:
        recommendation_response.append(await get_movie(movie_id=movie["movieId"]))
        recommendation_ratings.append(await get_rating(movie_id=movie["movieId"], user_id=str(user_id)))

    return {
        "userId": user_id,
        "recommended_movies": recommendation_response,
        "ratings": recommendation_ratings,
        "rating_counts": rating_counts,
        "preferences": preferences,
    }
