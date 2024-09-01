from __future__ import annotations
from typing import Optional, List
from pydantic import BaseModel
from ..movie_endpoint.model import ActorModel, GenreModel, ProductionCountryModel

class ShowModel(BaseModel):
    """
    A Pydantic model representing a show.

    Attributes:
    -----------
    id : str
        The unique identifier for the show.
    title : Optional[str]
        The title of the show.
    type : str
        The type of the show.
    age_certification : Optional[str]
        The age certification of the show.
    runtime : int
        The runtime of the show in minutes.
    seasons : int
        The number of seasons of the show.
    number_of_seasons : Optional[str]
        The number of seasons (nullable).
    imdb_id : Optional[str]
        The IMDb ID of the show.
    imdb_score : Optional[str]
        The IMDb score of the show.
    imdb_votes : Optional[int]
        The number of IMDb votes for the show.
    release_year : Optional[str]
        The release year of the show.
    duration : Optional[int]
        The duration of the show.
    is_movie_best_in_release_year : str
        Indicates if the show is the best in its release year.
    main_genre : Optional[str]
        The main genre of the show.
    main_production : Optional[str]
        The main production country of the show.
    actors : Optional[List[ActorModel]]
        The list of actors in the show.
    genres : Optional[List[GenreModel]]
        The list of genres of the show.
    production_countries : Optional[List[ProductionCountryModel]]
        The list of production countries of the show.
    """
    id: str
    title: Optional[str] = None
    type: str
    age_certification: Optional[str] = None
    runtime: int
    seasons: int
    number_of_seasons: Optional[str]
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


class ShowActorModel(BaseModel):
    """
    A Pydantic model representing a relationship between a show and an actor.

    Attributes:
    -----------
    show_id : str
        The ID of the show.
    name : int
        The ID of the actor.
    role : int
        The role ID of the actor in the show.
    """
    show_id: str
    name: int
    role: int

    class Config:
        arbitrary_types_allowed = True
