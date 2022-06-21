from fastapi import APIRouter, status, Body
from fastapi.encoders import jsonable_encoder
import auth.repository as AuthRepository
import auth.schema as AuthSchema

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(login_user: AuthSchema.LoginUser = Body(...)):
    return {"auth-status": await AuthRepository.login(jsonable_encoder(login_user))}
