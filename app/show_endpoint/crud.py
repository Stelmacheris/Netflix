from src.database.Models import Show, ShowActor, Actor, ShowProductionCountry, ShowGenres, show_production_country, show_genres
from sqlalchemy import Engine
from typing import List, Dict, Any
from app.common.CrudOperations import CrudOperations
from .model import ShowModel, ShowActorModel

class ShowCrud:
    """
    A class to perform CRUD operations specifically for shows.

    Attributes:
    -----------
    engine : Engine
        The database engine.
    cd : CrudOperations
        An instance of the CrudOperations class for generic CRUD operations.
    """

    def __init__(self, engine: Engine):
        """
        Initializes the ShowCrud with the given database engine.

        Parameters:
        -----------
        engine : Engine
            The database engine.
        """
        self.engine = engine
        self.cd = CrudOperations(self.engine)

    def get_all_shows(self) -> List[Dict[str, Any]]:
        """
        Retrieves all shows from the database.

        Returns:
        --------
        List[Dict[str, Any]]
            A list of dictionaries representing all shows.
        """
        return self.cd.get_all_items(Show)
        
    def get_show_by_id(self, id: str) -> Dict[str, Any]:
        """
        Retrieves a show by its ID from the database.

        Parameters:
        -----------
        id : str
            The ID of the show.

        Returns:
        --------
        Dict[str, Any]]
            A dictionary representing the show, or None if not found.
        """
        return self.cd.get_item_by_id(Show, id, Actor, ShowActor, ShowProductionCountry, show_production_country)
    
    def insert_show_into_database(self, show: ShowModel) -> None:
        """
        Inserts a new show into the database.

        Parameters:
        -----------
        show : ShowModel
            The show model to insert.
        """
        self.cd.insert_item_into_database(show, Show, ShowActor, ShowActorModel, ShowGenres, show_genres, ShowProductionCountry, show_production_country)
