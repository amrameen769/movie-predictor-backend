import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_utils.tasks import repeat_every

from config import settings

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Frontend Static Files Mounted - No Additional Frontend Server Required
# ui endpoint for build directory
app.mount("/ui", StaticFiles(directory="frontend", html=True), name="ui")
# static endpoint for ./build/static directory
app.mount("/static", StaticFiles(directory="./frontend/static"), name="static")

# Routes
from user.router import router as user_router
from auth.router import router as auth_router
from ai.router import router as ai_router

app.include_router(user_router)
app.include_router(auth_router)
app.include_router(ai_router)

import ai.repository as ai_repository


# @app.on_event("startup")
# async def KNNBasicModel():
#     await ai_repository.KNNBasicModel()
#
#
# @repeat_every(seconds=30 * 24 * 60 * 60)
# async def KNNBasicModel():
#     await ai_repository.KNNBasicModel()
#

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        reload=settings.DEBUG_MODE,
        port=settings.PORT,
    )
