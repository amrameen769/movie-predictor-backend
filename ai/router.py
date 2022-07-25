from fastapi import APIRouter, status, Body
from fastapi.encoders import jsonable_encoder
from pydantic import Field

import ai.schema as AISchema
import ai.repository as AIRepository

router = APIRouter(prefix="/ai", tags=["ai"])


@router.post("/add-movie", status_code=status.HTTP_200_OK)
async def add_movie(movie: AISchema.Movie = Body(...)):
    return await AIRepository.add_movie(jsonable_encoder(movie))


@router.post("/add-rating", status_code=status.HTTP_200_OK)
async def add_rating(rating: AISchema.Rating = Body(...)):
    return await AIRepository.add_rating(jsonable_encoder(rating))


@router.get("/recommend/user/{user_id}", status_code=status.HTTP_200_OK)
async def collab_recommend(user_id: int = Field(...)):
    return await AIRepository.collab_recommend(user_id)


@router.get("/get-movie/{movie_id}", status_code=status.HTTP_200_OK, response_model=AISchema.Movie)
async def get_movie(movie_id: str = Field(...)):
    return await AIRepository.get_movie(movie_id=movie_id)
