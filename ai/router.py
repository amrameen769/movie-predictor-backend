from fastapi import APIRouter, status, Body
from fastapi.encoders import jsonable_encoder
import ai.schema as AISchema
import ai.repository as AIRepository


router = APIRouter(prefix="/ai", tags=["ai"])


@router.post("/add-movie", status_code=status.HTTP_200_OK)
async def add_movie(movie: AISchema.Movie = Body(...)):
    return await AIRepository.add_movie(jsonable_encoder(movie))

@router.post("/add-rating", status_code=status.HTTP_200_OK)
async def add_rating(rating: AISchema.Rating = Body(...)):
    return await AIRepository.add_rating(jsonable_encoder(rating))

@router.get("/recommend", status_code=status.HTTP_200_OK)
async def collab_recommend(user_id=2):
    return await AIRepository.collab_recommend(user_id)