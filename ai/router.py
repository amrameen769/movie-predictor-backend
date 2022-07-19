from fastapi import APIRouter, status, Body
from fastapi.encoders import jsonable_encoder
import ai.schema as AISchema
import ai.repository as AIRepository

router = APIRouter(prefix="/ai", tags=["ai"])


@router.post("/add-movie", status_code=status.HTTP_200_OK)
async def add_movie(movie: AISchema.Movie = Body(...)):
    return await AIRepository.add_movie(jsonable_encoder(movie))
