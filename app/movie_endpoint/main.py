from fastapi import APIRouter
from .crud import MovieCrud
from src.database.PostgresConnection import PostgresConnection
from sqlalchemy import Engine
from .model import MovieModel,ActorModel
from typing import Union

router = APIRouter(
    prefix='/movie'
)

pc: PostgresConnection = PostgresConnection()
engine: Engine = pc.get_engine()
movie_crud: MovieCrud = MovieCrud(engine)

@router.get('/all',tags=['movie'])
async def get_all_movies():
    return movie_crud.get_all_movies()

@router.get('/{movie_id}',tags=['movie'])
async def get_movie_by_id(movie_id:str):
    return movie_crud.get_movie_by_id(movie_id)

@router.post('/',tags = ['movie'])
async def post_movie(movie: MovieModel):
    return movie_crud.insert_movie_into_database(movie)