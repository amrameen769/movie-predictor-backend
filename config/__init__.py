from typing import List

from pydantic import BaseSettings


class CommonSettings(BaseSettings):
    APP_NAME: str = "movie-predictor"
    DEBUG_MODE: bool = True
    TMDB_API_KEY: str = "ab67ab4af7ffc1d61ffde001fbdfbe2c"
    TMDB_URL: str = "https://api.themoviedb.org/3/"



class ServerSettings(BaseSettings):
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    ORIGINS: List[str] = [
        "https://127.0.0.1:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3000"
    ]


class DatabaseSettings(BaseSettings):
    # CLUSTER_URL: str = "mongodb://192.168.1.66:27017/"  # added remote host
    CLUSTER_URL: str = "mongodb://localhost:27017/"
    DB_PREFIX: str = "db_mp_"
    COL_PREFIX: str = "col_mp_"


class Settings(CommonSettings, DatabaseSettings, ServerSettings):
    pass


settings = Settings()
