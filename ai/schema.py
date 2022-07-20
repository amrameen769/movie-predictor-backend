from typing import Dict, List

from bson import ObjectId
from pydantic import BaseModel, Field

from database import PyObjectId


class Movie(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias='_id')
    movieId: str = Field(...)
    title: str = Field(...)
    genres: List[str] = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

        schema_extra = {
            "example": {
                "movieId": "111",
                "title": "Movie Title 1",
                "genres": ["a", "b", "c"]
            }
        }

class Rating(BaseModel):
    id: str = Field(alias='_id')
    userId: str = Field(...)
    movieId: str = Field(...)
    rating: str = Field(...)
    timestamp: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

        schema_extra = {
            "example": {
                "userId" :"1",
                "movieId" : "1",
                "rating" :"1.0",
                "timestamp" : "111111111"
            }
        }
