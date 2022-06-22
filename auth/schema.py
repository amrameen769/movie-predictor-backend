from lib2to3.pgen2 import token
from lib2to3.pytree import Base
from pydantic import BaseModel


class LoginUser(BaseModel):
  username: str
  password: str

  class Config():
    schema_extra = {
      "example": {
        "username": "janedoe/janedoe@amr.com",
        "password": "janedoe@123"
      }
    }

class Token(BaseModel):
  access_token: str
  token_type: str

class TokenData(BaseModel):
  username: str