from fastapi import APIRouter
from .crud import ShowCrud
from src.database.PostgresConnection import PostgresConnection
from sqlalchemy import Engine
from .model import ShowModel

router = APIRouter(
    prefix='/show'
)

pc: PostgresConnection = PostgresConnection()
engine: Engine = pc.get_engine()
show_crud: ShowCrud = ShowCrud(engine)

@router.get('/all',tags=['shows'])
async def get_all_movies():
    return show_crud.get_all_shows()

@router.get('/{show_id}',tags=['shows'])
async def get_show_by_id(show_id:str):
    return show_crud.get_show_by_id(show_id)

@router.post('/',tags=['shows'])
async def post_show(show: ShowModel):
    return show_crud.insert_show_into_database(show)
