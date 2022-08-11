from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from database import MotorDB
from hasher import Hasher

motor = MotorDB()
hasher = Hasher()


async def login(user: OAuth2PasswordRequestForm):
    await motor.connect_db(db_name="movie_predictor")
    user_col = await motor.get_collection(col_name="user")

    auth_user = await user_col.find_one(
        {"$or": [{"username": user.username}, {"email": user.username}]}
    )

    if not auth_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )

    return auth_user if hasher.verify_password(user.password, auth_user["password"]) else None


async def get_user(username: str):
    await motor.connect_db(db_name="movie_predictor")
    user_col = await motor.get_collection(col_name="user")

    auth_user = await user_col.find_one(
        {"$or": [{"username": username}, {"email": username}]}
    )

    return auth_user
