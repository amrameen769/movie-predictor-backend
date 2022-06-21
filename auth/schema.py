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