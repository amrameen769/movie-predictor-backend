from datetime import datetime, timedelta
from fastapi import Depends, status, HTTPException
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import auth.repository as AuthRepository
from auth.schema import TokenData


SECRET_KEY = "bd4c8f9a8b77a109679175ba7e84c4c76919d312319e0a49fada13c0e003381c"
ALGORITHM = "HS256"
ACCESS_TOKEN_TIMEOUT = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/auth-token")


def create_access_token(data: dict, expires_delta: timedelta or None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


async def token_auth(user_data: OAuth2PasswordRequestForm = Depends()):
    user = await AuthRepository.login(user_data)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_TIMEOUT)
    access_token = create_access_token(
        data={
            "sub": user["username"]
            if user["username"] == user_data.username
            else user_data.username
        },
        expires_delta=access_token_expires,
    )

    return {"access_token": access_token, "token_type": "bearer"}


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = await AuthRepository.get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user
