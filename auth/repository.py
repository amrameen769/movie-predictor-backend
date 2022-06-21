from fastapi import HTTPException, status
from database import MotorDB
from hasher import Hasher
import auth.schema as AuthSchema

motor = MotorDB()
hasher = Hasher()

async def login(user: AuthSchema.LoginUser):
    await motor.connect_db(db_name="movie_predictor")
    user_col = await motor.get_collection(col_name="user")

    auth_user = await user_col.find_one(
        {"$or": [{"username": user["username"]}, {"email": user["username"]}]}
    )

    if not auth_user:
      raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found.",
        )

    return hasher.verify_password(user["password"], auth_user["password"])