from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Body
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordRequestForm
from auth.jwt_token import token_auth

from auth.schema import Token

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/auth-token", status_code=status.HTTP_200_OK, response_model=Token)
async def token_authentication(login_user: OAuth2PasswordRequestForm = Depends()):
    return await token_auth(login_user)
