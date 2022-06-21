from bson import ObjectId
from pydantic import BaseModel, EmailStr, Field
from database import PyObjectId

class User(BaseModel):
  id : PyObjectId = Field(default_factory=PyObjectId, alias="_id")
  username: str = Field(...)
  email: EmailStr = Field(...)
  password: str = Field(...)
  
  class Config():
    allow_population_by_field_name = True
    arbitrary_types_allowed = True
    json_encoders = { ObjectId: str }

    schema_extra = {
      "example": {
        "username": "janedoe",
        "email": "janedoe@amr.com",
        "password": "janedoe@123"
      }
    }
  
class UserResponse(BaseModel):
  id: str = Field(alias="_id")
  username: str
  email: str

  class Config():
    orm_mode = True
