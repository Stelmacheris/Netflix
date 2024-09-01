from src.database.Models import Movie, MovieActor, Actor, MovieProductionCountry, MovieGenres, movie_production_country, movie_genres
from sqlalchemy import Engine
from typing import List, Dict, Any
from .model import MovieModel, MovieActorModel
from app.common.CrudOperations import CrudOperations

class MovieCrud:
    """
    A class to perform CRUD operations specifically for movies.

    Attributes:
    -----------
    engine : Engine
        The database engine.
    cd : CrudOperations
        An instance of the CrudOperations class for generic CRUD operations.
    """

    def __init__(self, engine: Engine):
        """
        Initializes the MovieCrud with the given database engine.

        Parameters:
        -----------
        engine : Engine
            The database engine.
        """
        self.engine = engine
        self.cd = CrudOperations(self.engine)

    def get_all_movies(self) -> List[Dict[str, Any]]:
        """
        Retrieves all movies from the database.

        Returns:
        --------
        List[Dict[str, Any]]
            A list of dictionaries representing all movies.
        """
        return self.cd.get_all_items(Movie)
        
    def get_movie_by_id(self, id: str) -> Dict[str, Any]:
        """
        Retrieves a movie by its ID from the database.

        Parameters:
        -----------
        id : str
            The ID of the movie.

        Returns:
        --------
        Dict[str, Any]
            A dictionary representing the movie, or None if not found.
        """
        return self.cd.get_item_by_id(Movie, id, Actor, MovieActor, MovieProductionCountry, movie_production_country)
        
    def insert_movie_into_database(self, movie: MovieModel) -> None:
        """
        Inserts a new movie into the database.

        Parameters:
        -----------
        movie : MovieModel
            The movie model to insert.
        """
        self.cd.insert_item_into_database(movie, Movie, MovieActor, MovieActorModel, MovieGenres, movie_genres, MovieProductionCountry, movie_production_country)
