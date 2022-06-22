from fastapi import HTTPException, status
from hasher import Hasher
import user.schema as UserSchema
from database import MotorDB

motor = MotorDB()
hasher = Hasher()

async def check_existing_user(username: str, email: str):
  await motor.connect_db(db_name="movie_predictor")
  user_col = await motor.get_collection(col_name="user")

  auth_user = await user_col.find_one(
      {"$or": [{"username": username}, {"email": email}]}
  )

  return True if auth_user else False 


async def create_user(user: UserSchema.User):
    await motor.connect_db(db_name="movie_predictor")
    user_col = await motor.get_collection(col_name="user")

    existing_user = await check_existing_user(
        username=user["username"], email=user["email"]
    )

    if not existing_user:
        user["password"] = hasher.get_hashed_password(user["password"])
        # hashing is only required if new user data is not existing
        new_user = await user_col.insert_one(user)

        if not new_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User Creation failed", # corrected typo
            )
        else:
            created_user = await user_col.find_one({"_id": new_user.inserted_id})

            return created_user
    else:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail=f"User already exists with the same username or password, Please login.",
        )



