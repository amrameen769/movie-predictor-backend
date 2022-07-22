from fastapi import HTTPException, status

import ai.schema as AISchema
from database import MotorDB
import pandas as pd

motor = MotorDB()


async def add_movie(movie: AISchema.Movie):
    await motor.connect_db(db_name="movie_predictor")
    movie_col = await motor.get_collection(col_name="movie")

    if movie_col is not None:
        new_movie = await movie_col.insert_one(movie)
        if not new_movie:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Movie creation failed"
            )
        else:
            created_movie = await movie_col.find_one({"_id": new_movie.inserted_id})

            return created_movie

async def add_rating(rating: AISchema.Rating):
    await motor.connect_db(db_name="movie_predictor")
    rating_col = await motor.get_collection(col_name="rating")

    if rating_col is not None:
        new_rating = await rating_col.insert_one(rating)
        if not new_rating:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Rating creation failed"
            )
        else:
            created_rating = await rating_col.find_one({"_id": new_rating.inserted_id})
            return created_rating

async def to_df(list_of_docs):
    df = pd.json_normalize(list_of_docs)
    df.drop(['_id'], axis=1, inplace=True)
    return df

async def get_all_rating():
    from surprise import Reader, Dataset

    await motor.connect_db(db_name="movie_predictor")
    rating_col = await motor.get_collection(col_name="rating")

    size = await rating_col.count_documents({})

    ratingset = []
    cursor = rating_col.find({})
    for doc in await cursor.to_list(size):
        ratingset.append(doc)
    df = await to_df(ratingset)

    reader = Reader(rating_scale=(1,5))
    dataset = Dataset.load_from_df(df[["userId", "movieId", "rating"]], reader=reader)
    return(dataset)

def load_model(model_filename):
    from surprise import dump
    import os
    file_name = os.path.expanduser(model_filename)
    _, loaded_model = dump.load(file_name)
    return loaded_model

async def movieid_to_name(movieID):
    await motor.connect_db(db_name="movie_predictor")
    movie_col = await motor.get_collection(col_name="movie")

    cursor = movie_col.find({ "movieId" : str(movieID)})
    for doc in await cursor.to_list(10):
        return doc["title"]