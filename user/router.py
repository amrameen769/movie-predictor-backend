from fastapi import APIRouter, Body, Depends, status
from fastapi.encoders import jsonable_encoder

import user.repository as UserRepository
import user.schema as UserSchema
from auth.jwt_token import get_current_user

router = APIRouter(prefix="/user", tags=["User"])


@router.post(
    "/create",
    status_code=status.HTTP_201_CREATED,
    response_model=UserSchema.UserResponse,
)
async def create(user: UserSchema.User = Body(...)):
    return await UserRepository.create_user(jsonable_encoder(user))


@router.get("/me", status_code=status.HTTP_200_OK, response_model=UserSchema.UserResponse)
async def get_me(current_user: UserSchema.UserResponse = Depends(get_current_user)):
    return current_user
