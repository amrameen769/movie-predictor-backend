from datetime import datetime
from typing import Dict, List, Optional

from bson import ObjectId
from pydantic import BaseModel, Field

from database import PyObjectId


class ConfigModel(BaseModel):
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class Movie(ConfigModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias='_id')
    movieId: str = Field(...)
    title: str = Field(...)
    genres: List[str] = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "movieId": "111",
                "title": "Movie Title 1",
                "genres": ["a", "b", "c"]
            }
        }


class Rating(ConfigModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias='_id')
    userId: str = Field(...)
    movieId: str = Field(...)
    rating: str = Field(...)
    timestamp: Optional[datetime] = datetime.now()

    class Config:
        schema_extra = {
            "example": {
                "userId": "1",
                "movieId": "1",
                "rating": "1.0",
                "timestamp": "111111111"
            }
        }


class Comment(BaseModel):
    userId: str = Field(...)
    timestamp: Optional[datetime] = datetime.now()
    comment: str = Field(...)


class Forum(ConfigModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias='_id')
    movieId: str = Field(...)
    comments: List[Comment] = Field(...)


class Preferences(ConfigModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias='_id')
    userId: str = Field(...)
    preferences: List[str] = Field(...)


