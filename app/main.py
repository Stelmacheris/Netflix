from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from .movie_endpoint.main import router as movie_router
from .show_endpoint.main import router as show_router

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:5173",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

app.include_router(movie_router)
app.include_router(show_router)

@app.get("/")
async def root():
    return {"message": "Hello World"}