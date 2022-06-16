from typing import List
from pydantic import BaseSettings


class CommonSettings(BaseSettings):
  APP_NAME: str = "movie-predictor"
  DEBUG_MODE: bool = True

class ServerSettings(BaseSettings):
  HOST: str = "0.0.0.0"
  PORT: int = 8000
  ORIGINS: List[str] = [
    "https://127.0.0.1:3000",
    "http://127.0.0.1:3000"
  ]

class DatabaseSettings(BaseSettings):
  CLUSTER_URL: str = "mongodb://localhost:27017/"

class Settings(CommonSettings, DatabaseSettings, ServerSettings):
  pass

settings = Settings()
