from typing import List

from fastapi import APIRouter, status, Body, Depends
from fastapi.encoders import jsonable_encoder
from pydantic import Field

import ai.schema as AISchema
import ai.repository as AIRepository
import user.schema as UserSchema
from auth.jwt_token import get_current_user

router = APIRouter(prefix="/ai", tags=["ai"])


@router.post("/add-movie", status_code=status.HTTP_200_OK)
async def add_movie(movie: AISchema.Movie = Body(...)):
    return await AIRepository.add_movie(jsonable_encoder(movie))


@router.post("/add-rating", status_code=status.HTTP_200_OK)
async def add_rating(rating: AISchema.Rating = Body(...)):
    return await AIRepository.add_rating(rating)


# for authenticated user
@router.get("/recommend/user", status_code=status.HTTP_200_OK)
async def collab_recommend_auth(current_user: UserSchema.UserResponse = Depends(get_current_user)):
    return await AIRepository.collab_recommend(current_user["userId"])


@router.get("/recommend/user/{user_id}", status_code=status.HTTP_200_OK)
async def collab_recommend(user_id: int):
    return await AIRepository.collab_recommend(user_id)


@router.get("/get-movie/{movie_id}", status_code=status.HTTP_200_OK)
async def get_movie(movie_id: str = Field(...)):
    return await AIRepository.get_movie(movie_id=movie_id)


@router.post("/add-comment/{movie_id}", status_code=status.HTTP_201_CREATED)
async def add_comment(comment: AISchema.Comment = Body(...), movie_id: str = Field(...)):
    return await AIRepository.add_comments(comment=comment, movie_id=movie_id)


@router.get("/get-comments/{movie_id}", status_code=status.HTTP_200_OK)
async def get_comments(movie_id: str = Field(...)):
    return await AIRepository.get_comments(movie_id=movie_id)


@router.get("/get-all-user-rating/{user_id}", status_code=status.HTTP_200_OK)
async def get_all_user_rating(user_id: str = Field(...)):
    return await AIRepository.get_users_rating_all(user_id)


@router.post("/add-user-preferences/{user_id}", status_code=status.HTTP_201_CREATED)
async def add_user_preferences(user_id: str = Field(...), preferences: List[str] = Body(...)):
    return await AIRepository.add_user_preferences(user_id=user_id, preferences=preferences)


@router.get("/get-preferences", status_code=status.HTTP_200_OK)
async def update_watchlist(current_user: UserSchema.UserResponse = Depends(get_current_user)):
    return await AIRepository.get_user_preferences(current_user["userId"])


@router.post("/update-watchlist/{user_id}", status_code=status.HTTP_201_CREATED)
async def update_watchlist(user_id: str = Field(...), movie_ids: List[str] = Body(...)):
    return await AIRepository.add_to_watchlist(user_id=user_id, movie_ids=movie_ids)


@router.get("/get-watchlist/{user_id}", status_code=status.HTTP_200_OK)
async def update_watchlist(user_id: str = Field(...)):
    return await AIRepository.get_watchlist(user_id=user_id)


@router.get("/content-recommend", status_code=status.HTTP_200_OK)
async def contend_recommend(genres: str, user_id: str):
    return await AIRepository.content_recommend(genres=genres, user_id=user_id)
