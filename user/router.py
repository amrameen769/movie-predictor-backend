from fastapi import APIRouter, Body, status
from fastapi.encoders import jsonable_encoder
import user.repository as UserRepository

import user.schema as UserSchema

router = APIRouter(prefix="/user", tags=["User"])


@router.post(
    "/create", status_code=status.HTTP_201_CREATED, response_model=UserSchema.UserResponse
)
async def create(user: UserSchema.User = Body(...)):
    return await UserRepository.create_user(jsonable_encoder(user))
