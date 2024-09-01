from __future__ import annotations
from typing import Optional, List
from pydantic import BaseModel

class MovieModel(BaseModel):
    """
    A Pydantic model representing a movie.

    Attributes:
    -----------
    id : str
        The unique identifier for the movie.
    title : Optional[str]
        The title of the movie.
    type : str
        The type of the movie.
    age_certification : Optional[str]
        The age certification of the movie.
    runtime : int
        The runtime of the movie in minutes.
    imdb_id : Optional[str]
        The IMDb ID of the movie.
    imdb_score : Optional[str]
        The IMDb score of the movie.
    imdb_votes : Optional[int]
        The number of IMDb votes for the movie.
    release_year : Optional[str]
        The release year of the movie.
    duration : Optional[int]
        The duration of the movie.
    is_movie_best_in_release_year : str
        Indicates if the movie is the best in its release year.
    main_genre : Optional[str]
        The main genre of the movie.
    main_production : Optional[str]
        The main production country of the movie.
    actors : Optional[List[ActorModel]]
        The list of actors in the movie.
    genres : Optional[List[GenreModel]]
        The list of genres of the movie.
    production_countries : Optional[List[ProductionCountryModel]]
        The list of production countries of the movie.
    """
    id: str
    title: Optional[str] = None
    type: str
    age_certification: Optional[str] = None
    runtime: int
    imdb_id: Optional[str]
    imdb_score: Optional[str]
    imdb_votes: Optional[int] = None
    release_year: Optional[str] = None
    duration: Optional[int] = None
    is_movie_best_in_release_year: str
    main_genre: Optional[str] = None
    main_production: Optional[str] = None
    actors: Optional[List[ActorModel]] = None
    genres: Optional[List[GenreModel]] = None
    production_countries: Optional[List[ProductionCountryModel]] = None

    class Config:
        arbitrary_types_allowed = True


class ActorModel(BaseModel):
    """
    A Pydantic model representing an actor.

    Attributes:
    -----------
    name : str
        The name of the actor.
    """
    name: str

    class Config:
        arbitrary_types_allowed = True


class MovieActorModel(BaseModel):
    """
    A Pydantic model representing a relationship between a movie and an actor.

    Attributes:
    -----------
    movie_id : str
        The ID of the movie.
    name : int
        The ID of the actor.
    role : int
        The role ID of the actor in the movie.
    """
    movie_id: str
    name: int
    role: int

    class Config:
        arbitrary_types_allowed = True


class GenreModel(BaseModel):
    """
    A Pydantic model representing a genre.

    Attributes:
    -----------
    genre : str
        The name of the genre.
    """
    genre: str

    class Config:
        arbitrary_types_allowed = True


class ProductionCountryModel(BaseModel):
    """
    A Pydantic model representing a production country.

    Attributes:
    -----------
    production_country : str
        The name of the production country.
    """
    production_country: str

    class Config:
        arbitrary_types_allowed = True
