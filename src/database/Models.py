from __future__ import annotations
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Column, Table, ForeignKey, Integer
from typing import Optional, List

Base = declarative_base()

# Association tables for many-to-many relationships
movie_genres = Table(
    "movie_genre_link",
    Base.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column("movie_id", ForeignKey("movie.id")),
    Column("genre_id", ForeignKey("movie_genre.id")),
)

movie_production_country = Table(
    'movie_production_country_link',
    Base.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column("movie_id", ForeignKey("movie.id")),
    Column("production_country_id", ForeignKey("movie_production_country.id")),    
)

show_genres = Table(
    "show_genre_link",
    Base.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column("show_id", ForeignKey("show.id")),
    Column("genre_id", ForeignKey("show_genre.id")),
)

show_production_country = Table(
    'show_production_country_link',
    Base.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column("show_id", ForeignKey("show.id")),
    Column("production_country_id", ForeignKey("show_production_country.id")),    
)


class Movie(Base):
    """
    Represents a movie entity in the database.
    
    Attributes:
    -----------
    id : Mapped[str]
        The primary key of the movie.
    title : Mapped[Optional[str]]
        The title of the movie.
    type : Mapped[str]
        The type of movie.
    age_certification : Mapped[Optional[str]]
        The age certification of the movie.
    runtime : Mapped[int]
        The runtime of the movie.
    imdb_id : Mapped[Optional[str]]
        The IMDb ID of the movie.
    imdb_score : Mapped[Optional[str]]
        The IMDb score of the movie.
    imdb_votes : Mapped[Optional[int]]
        The number of IMDb votes for the movie.
    release_year : Mapped[Optional[str]]
        The release year of the movie.
    duration : Mapped[Optional[int]]
        The duration of the movie.
    is_movie_best_in_release_year : Mapped[str]
        Indicates if the movie is the best in its release year.
    main_genre : Mapped[Optional[str]]
        The main genre of the movie.
    main_production : Mapped[Optional[str]]
        The main production country of the movie.
    movie_genres : Mapped[List[MovieGenres]]
        The genres associated with the movie.
    movie_production_countries : Mapped[List[MovieProductionCountry]]
        The production countries associated with the movie.
    movie_actor : Mapped[List[MovieActor]]
        The actors associated with the movie.
    """
    __tablename__ = 'movie'
    id: Mapped[str] = mapped_column(primary_key=True)
    title: Mapped[Optional[str]] = mapped_column(nullable=True)
    type: Mapped[str]
    age_certification: Mapped[Optional[str]] = mapped_column(nullable=True)
    runtime: Mapped[int]
    imdb_id: Mapped[Optional[str]] = mapped_column(nullable=True)
    imdb_score: Mapped[Optional[str]] = mapped_column(nullable=True)
    imdb_votes: Mapped[Optional[int]] = mapped_column(nullable=True)
    release_year: Mapped[Optional[str]] = mapped_column(nullable=True)
    duration: Mapped[Optional[int]] = mapped_column(nullable=True)
    is_movie_best_in_release_year: Mapped[str]
    main_genre: Mapped[Optional[str]] = mapped_column(nullable=True)
    main_production: Mapped[Optional[str]] = mapped_column(nullable=True)

    movie_genres: Mapped[List[MovieGenres]] = relationship(secondary=movie_genres, back_populates='movie')
    movie_production_countries: Mapped[List[MovieProductionCountry]] = relationship(secondary=movie_production_country, back_populates='movie')
    movie_actor: Mapped[List[MovieActor]] = relationship()

    def __repr__(self):
        return f'{self.id}, {self.main_genre}, {self.main_production}'


class MovieActor(Base):
    """
    Represents a movie actor entity in the database.

    Attributes:
    -----------
    id : Mapped[int]
        The primary key of the movie actor.
    movie_id : Mapped[str]
        The ID of the movie.
    name : Mapped[int]
        The ID of the actor.
    role : Mapped[int]
        The ID of the role.
    """
    __tablename__ = 'movie_actor'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    movie_id: Mapped[str] = mapped_column(ForeignKey('movie.id'))
    name: Mapped[int] = mapped_column(ForeignKey('actor.id'))
    role: Mapped[int] = mapped_column(ForeignKey('role.id'))


class ShowActor(Base):
    """
    Represents a show actor entity in the database.

    Attributes:
    -----------
    id : Mapped[int]
        The primary key of the show actor.
    show_id : Mapped[str]
        The ID of the show.
    name : Mapped[int]
        The ID of the actor.
    role : Mapped[int]
        The ID of the role.
    """
    __tablename__ = 'show_actor'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    show_id: Mapped[str] = mapped_column(ForeignKey('show.id'))
    name: Mapped[int] = mapped_column(ForeignKey('actor.id'))
    role: Mapped[int] = mapped_column(ForeignKey('role.id'))


class Show(Base):
    """
    Represents a show entity in the database.

    Attributes:
    -----------
    id : Mapped[str]
        The primary key of the show.
    title : Mapped[str]
        The title of the show.
    type : Mapped[str]
        The type of show.
    age_certification : Mapped[Optional[str]]
        The age certification of the show.
    runtime : Mapped[int]
        The runtime of the show.
    seasons : Mapped[int]
        The number of seasons of the show.
    number_of_seasons : Mapped[int]
        The number of seasons of the show (nullable).
    imdb_id : Mapped[Optional[str]]
        The IMDb ID of the show.
    imdb_score : Mapped[Optional[str]]
        The IMDb score of the show.
    imdb_votes : Mapped[Optional[int]]
        The number of IMDb votes for the show.
    release_year : Mapped[Optional[str]]
        The release year of the show.
    duration : Mapped[Optional[int]]
        The duration of the show.
    is_movie_best_in_release_year : Mapped[str]
        Indicates if the show is the best in its release year.
    main_genre : Mapped[Optional[str]]
        The main genre of the show.
    main_production : Mapped[Optional[str]]
        The main production country of the show.
    show_genres : Mapped[List[ShowGenres]]
        The genres associated with the show.
    show_production_countries : Mapped[List[ShowProductionCountry]]
        The production countries associated with the show.
    show_actor : Mapped[List[ShowActor]]
        The actors associated with the show.
    """
    __tablename__ = 'show'
    id: Mapped[str] = mapped_column(primary_key=True)
    title: Mapped[str]
    type: Mapped[str]
    age_certification: Mapped[Optional[str]] = mapped_column(nullable=True)
    runtime: Mapped[int]
    seasons: Mapped[int]
    number_of_seasons: Mapped[int] = mapped_column(nullable=True)
    imdb_id: Mapped[Optional[str]] = mapped_column(nullable=True)
    imdb_score: Mapped[Optional[str]] = mapped_column(nullable=True)
    imdb_votes: Mapped[Optional[int]] = mapped_column(nullable=True)
    release_year: Mapped[Optional[str]] = mapped_column(nullable=True)
    duration: Mapped[Optional[int]] = mapped_column(nullable=True)
    is_movie_best_in_release_year: Mapped[str]
    main_genre: Mapped[Optional[str]] = mapped_column(nullable=True)
    main_production: Mapped[Optional[str]] = mapped_column(nullable=True)

    show_genres: Mapped[List[ShowGenres]] = relationship(secondary=show_genres, back_populates='show')
    show_production_countries: Mapped[List[ShowProductionCountry]] = relationship(secondary=show_production_country, back_populates='show')
    show_actor: Mapped[List[ShowActor]] = relationship()


class MovieGenres(Base):
    """
    Represents a movie genre entity in the database.

    Attributes:
    -----------
    id : Mapped[int]
        The primary key of the movie genre.
    genre : Mapped[str]
        The genre of the movie.
    movie : Mapped[List[Movie]]
        The movies associated with this genre.
    """
    __tablename__ = 'movie_genre'
    id: Mapped[int] = mapped_column(primary_key=True)
    genre: Mapped[str]
    movie: Mapped[List[Movie]] = relationship(secondary=movie_genres, back_populates='movie_genres')


class MovieProductionCountry(Base):
    """
    Represents a movie production country entity in the database.

    Attributes:
    -----------
    id : Mapped[int]
        The primary key of the production country.
    production_country : Mapped[str]
        The name of the production country.
    movie : Mapped[List[Movie]]
        The movies associated with this production country.
    """
    __tablename__ = 'movie_production_country'
    id: Mapped[int] = mapped_column(primary_key=True)
    production_country: Mapped[str]
    movie: Mapped[List[Movie]] = relationship(secondary=movie_production_country, back_populates='movie_production_countries')


class ShowGenres(Base):
    """
    Represents a show genre entity in the database.

    Attributes:
    -----------
    id : Mapped[int]
        The primary key of the show genre.
    genre : Mapped[str]
        The genre of the show.
    show : Mapped[List[Show]]
        The shows associated with this genre.
    """
    __tablename__ = 'show_genre'
    id: Mapped[int] = mapped_column(primary_key=True)
    genre: Mapped[str]
    show: Mapped[List[Show]] = relationship(secondary=show_genres, back_populates='show_genres')


class ShowProductionCountry(Base):
    """
    Represents a show production country entity in the database.

    Attributes:
    -----------
    id : Mapped[int]
        The primary key of the production country.
    production_country : Mapped[str]
        The name of the production country.
    show : Mapped[List[Show]]
        The shows associated with this production country.
    """
    __tablename__ = 'show_production_country'
    id: Mapped[int] = mapped_column(primary_key=True)
    production_country: Mapped[str]
    show: Mapped[List[Show]] = relationship(secondary=show_production_country, back_populates='show_production_countries')


class Credit(Base):
    """
    Represents a credit entity in the database.

    Attributes:
    -----------
    id : Mapped[int]
        The primary key of the credit.
    character : Mapped[Optional[str]]
        The character associated with the credit.
    """
    __tablename__ = 'credit'
    id: Mapped[int] = mapped_column(primary_key=True)
    character: Mapped[Optional[str]] = mapped_column(nullable=True)  


class Actor(Base):
    """
    Represents an actor entity in the database.

    Attributes:
    -----------
    id : Mapped[int]
        The primary key of the actor.
    name : Mapped[Optional[str]]
        The name of the actor.
    movie_actor : Mapped[List[MovieActor]]
        The movie actor associations.
    show_actor : Mapped[List[ShowActor]]
        The show actor associations.
    """
    __tablename__ = 'actor'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[Optional[str]] = mapped_column(nullable=True)
    movie_actor: Mapped[List[MovieActor]] = relationship()  
    show_actor: Mapped[List[ShowActor]] = relationship()  


class Role(Base):
    """
    Represents a role entity in the database.

    Attributes:
    -----------
    id : Mapped[int]
        The primary key of the role.
    role : Mapped[str]
        The name of the role.
    movie_actor : Mapped[List[MovieActor]]
        The movie actor associations.
    show_actor : Mapped[List[ShowActor]]
        The show actor associations.
    """
    __tablename__ = 'role'
    id: Mapped[int] = mapped_column(primary_key=True)
    role: Mapped[str]
    movie_actor: Mapped[List[MovieActor]] = relationship()
    show_actor: Mapped[List[ShowActor]] = relationship()    
