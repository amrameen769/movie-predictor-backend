from fastapi import HTTPException, status

import ai.schema as AISchema
from database import MotorDB

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