from typing import Dict, Any, Type, List
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from src.database.Models import Movie, Actor, Show, MovieGenres, MovieProductionCountry

class CrudOperations:
    """
    A class to perform CRUD operations on a database using SQLAlchemy.

    Attributes:
    -----------
    engine : Any
        The database engine.
    """

    def __init__(self, engine):
        """
        Initializes the CrudOperations with the given database engine.

        Parameters:
        -----------
        engine : Any
            The database engine.
        """
        self.engine = engine

    def get_all_items(self, item_class: Type[Any]) -> List[Dict[str, Any]]:
        """
        Retrieves all items of a given class from the database.

        Parameters:
        -----------
        item_class : Type[Any]
            The class of the items to retrieve.

        Returns:
        --------
        List[Dict[str, Any]]
            A list of dictionaries representing the items.
        """
        with Session(bind=self.engine) as session:
            items = session.query(item_class).all()
            return items

    def get_item_by_id(self, item_class: Type[Any], id: str, actor_class: Type[Any], actor_relation: Type[Any], production_country_class: Type[Any], production_relation: Any) -> Dict[str, Any]:
        """
        Retrieves an item by its ID from the database, including related actors and production countries.

        Parameters:
        -----------
        item_class : Type[Any]
            The class of the item to retrieve.
        id : str
            The ID of the item.
        actor_class : Type[Any]
            The class of the actors related to the item.
        actor_relation : Type[Any]
            The relation class for actors.
        production_country_class : Type[Any]
            The class of the production countries related to the item.
        production_relation : Any
            The relation table for production countries.

        Returns:
        --------
        Dict[str, Any]
            A dictionary representing the item, or None if not found.
        """
        with Session(bind=self.engine) as session:
            item = session.query(item_class).filter(item_class.id == id).first()
            if item:
                item_dict = self.to_dict(item)
                item_dict['actors'] = self.get_item_actors(item.id, actor_class, actor_relation)
                item_dict['production_countries'] = self.get_item_production_countries(item.id, production_country_class, production_relation)
                return item_dict
            return None

    def get_item_actors(self, item_id: str, actor_class: Type[Any], actor_relation: Type[Any]) -> List[Dict[str, Any]]:
        """
        Retrieves the actors related to a given item ID.

        Parameters:
        -----------
        item_id : str
            The ID of the item.
        actor_class : Type[Any]
            The class of the actors.
        actor_relation : Type[Any]
            The relation class for actors.

        Returns:
        --------
        List[Dict[str, Any]]
            A list of dictionaries representing the actors.
        """
        with Session(bind=self.engine) as session:
            if hasattr(actor_relation, 'movie_id'):
                filter_condition = actor_relation.movie_id == item_id
            else:
                filter_condition = actor_relation.show_id == item_id

            actors = session.query(actor_class).join(actor_relation, actor_class.id == actor_relation.id).filter(filter_condition).all()
            return [self.to_dict(actor) for actor in actors]

    def get_item_production_countries(self, item_id: str, production_country_class: Type[Any], production_relation: Any) -> List[Dict[str, Any]]:
        """
        Retrieves the production countries related to a given item ID.

        Parameters:
        -----------
        item_id : str
            The ID of the item.
        production_country_class : Type[Any]
            The class of the production countries.
        production_relation : Any
            The relation table for production countries.

        Returns:
        --------
        List[Dict[str, Any]]
            A list of dictionaries representing the production countries.
        """
        if hasattr(production_relation.c, 'movie_id'):
            filter_condition = production_relation.c.movie_id == item_id
        else:
            filter_condition = production_relation.c.show_id == item_id
        with Session(bind=self.engine) as session:
            production_countries = session.query(production_country_class).join(production_relation, production_country_class.id == production_relation.c.production_country_id).filter(filter_condition).all()
            return [self.to_dict(production_country) for production_country in production_countries]

    def insert_item_into_database(self, item: Any, item_model: Type[Any], actor_model: Type[Any], actor_relation_model: Type[Any], genre_model: Type[Any], genre_relation_table: Any, production_country_model: Type[Any], production_country_relation_table: Any) -> None:
        """
        Inserts a new item into the database, including related actors, genres, and production countries.

        Parameters:
        -----------
        item : Any
            The item to insert.
        item_model : Type[Any]
            The model class for the item.
        actor_model : Type[Any]
            The model class for actors.
        actor_relation_model : Type[Any]
            The relation model class for actors.
        genre_model : Type[Any]
            The model class for genres.
        genre_relation_table : Any
            The relation table for genres.
        production_country_model : Type[Any]
            The model class for production countries.
        production_country_relation_table : Any
            The relation table for production countries.
        """
        db_item = item_model(**item.model_dump(exclude={"actors", "genres", "production_countries"}))
        with Session(bind=self.engine) as session:
            session.add(db_item)
            session.commit()
            session.refresh(db_item)
            for actor in item.actors:
                db_actor = self.add_actor(session, actor)
                item_actor = self.create_actor_relation(actor_relation_model, db_item.id, db_actor.id, item_model)
                self.add_actor_relation(session, item_actor, actor_model)
            self.add_genre_relation(session, item.genres, db_item.id, genre_model, genre_relation_table)
            self.add_production_country_relation(session, item.production_countries, db_item.id, production_country_model, production_country_relation_table)

    def create_actor_relation(self, actor_relation_model: Type[Any], item_id: int, actor_id: int, item_type: Any) -> Any:
        """
        Creates a new actor relation for a given item.

        Parameters:
        -----------
        actor_relation_model : Type[Any]
            The relation model class for actors.
        item_id : int
            The ID of the item.
        actor_id : int
            The ID of the actor.
        item_type : Any
            The type of the item (Movie or Show).

        Returns:
        --------
        Any
            The created actor relation.
        """
        if item_type == Movie:
            return actor_relation_model(movie_id=item_id, name=actor_id, role=1)
        elif item_type == Show:
            return actor_relation_model(show_id=item_id, name=actor_id, role=1)
        else:
            raise ValueError("Unknown item type")
        
    def create_genre_relation(self, actor_relation_model: Type[Any], item_id: int, actor_id: int, item_type: Any) -> Any:
        """
        Creates a new genre relation for a given item.

        Parameters:
        -----------
        actor_relation_model : Type[Any]
            The relation model class for genres.
        item_id : int
            The ID of the item.
        actor_id : int
            The ID of the genre.
        item_type : Any
            The type of the item (Movie or Show).

        Returns:
        --------
        Any
            The created genre relation.
        """
        if item_type == Movie:
            return actor_relation_model(movie_id=item_id, name=actor_id, role=1)
        elif item_type == Show:
            return actor_relation_model(show_id=item_id, name=actor_id, role=1)
        else:
            raise ValueError("Unknown item type")

    def add_actor(self, session: Session, actor: Any) -> Any:
        """
        Adds a new actor to the database, or retrieves the existing one.

        Parameters:
        -----------
        session : Session
            The database session.
        actor : Any
            The actor to add.

        Returns:
        --------
        Any
            The added or existing actor.
        """
        db_actor = session.query(Actor).filter(Actor.name == actor.name).first()
        if db_actor:
            return db_actor
        db_actor = Actor(**actor.model_dump())
        db_actor.id = self.get_max_id(session, Actor) + 1
        session.add(db_actor)
        session.commit()
        session.refresh(db_actor)
        return db_actor
    
    def add_actor_relation(self, session: Session, actor_relation: Any, actor_model: Type[Any]) -> None:
        """
        Adds a new actor relation to the database.

        Parameters:
        -----------
        session : Session
            The database session.
        actor_relation : Any
            The actor relation to add.
        actor_model : Type[Any]
            The model class for actors.
        """
        db_actor_relation = actor_model(**actor_relation.model_dump())
        db_actor_relation.id = self.get_max_id(session, actor_model) + 1
        session.add(db_actor_relation)
        session.commit()

    def add_genre_relation(self, session: Session, genres_list: List[Any], item_id: int, genre_model: Type[Any], genre_relation_table: Any) -> None:
        """
        Adds new genre relations to the database for a given item.

        Parameters:
        -----------
        session : Session
            The database session.
        genres_list : List[Any]
            The list of genres.
        item_id : int
            The ID of the item.
        genre_model : Type[Any]
            The model class for genres.
        genre_relation_table : Any
            The relation table for genres.
        """
        for genre_name in genres_list:
            genre = session.query(genre_model).filter(genre_model.genre == genre_name.genre).first()
            
            if not genre:
                genre = genre_model()
                genre.genre = genre_name.genre
                genre.id = self.get_max_id(session, genre_model) + 1
                session.add(genre)
                session.commit()
            self.execution_statment_genre(genre_model, session, genre_relation_table, item_id, genre)
            session.commit()

    def add_production_country_relation(self, session: Session, production_countries_list: List[Any], item_id: int, production_country_model: Type[Any], production_country_relation_table: Any) -> None:
        """
        Adds new production country relations to the database for a given item.

        Parameters:
        -----------
        session : Session
            The database session.
        production_countries_list : List[Any]
            The list of production countries.
        item_id : int
            The ID of the item.
        production_country_model : Type[Any]
            The model class for production countries.
        production_country_relation_table : Any
            The relation table for production countries.
        """
        for production_country in production_countries_list:
            pc = session.query(production_country_model).filter(production_country_model.production_country == production_country.production_country).first()
            
            if not pc:
                pc = production_country_model()
                pc.production_country = production_country.production_country
                pc.id = self.get_max_id(session, production_country_model) + 1
                session.add(pc)
                session.commit()
            self.execution_statment_pc(production_country_model, session, production_country_relation_table, item_id, pc)
            session.commit()

    def execution_statment_genre(self, item_type: Type[Any], session: Session, genre_relation_table: Any, item_id: int, genre: Any) -> None:
        """
        Executes the statement to add a genre relation to the database.

        Parameters:
        -----------
        item_type : Type[Any]
            The type of the item (MovieGenres or ShowGenres).
        session : Session
            The database session.
        genre_relation_table : Any
            The relation table for genres.
        item_id : int
            The ID of the item.
        genre : Any
            The genre to relate.
        """
        if item_type == MovieGenres:
            session.execute(genre_relation_table.insert().values(movie_id=item_id, genre_id=genre.id))
        else:
            session.execute(genre_relation_table.insert().values(show_id=item_id, genre_id=genre.id))

    def execution_statment_pc(self, item_type: Type[Any], session: Session, production_country_relation_table: Any, item_id: int, pc: Any) -> None:
        """
        Executes the statement to add a production country relation to the database.

        Parameters:
        -----------
        item_type : Type[Any]
            The type of the item (MovieProductionCountry or ShowProductionCountry).
        session : Session
            The database session.
        production_country_relation_table : Any
            The relation table for production countries.
        item_id : int
            The ID of the item.
        pc : Any
            The production country to relate.
        """
        if item_type == MovieProductionCountry:
            session.execute(production_country_relation_table.insert().values(movie_id=item_id, production_country_id=pc.id))
        else:
            session.execute(production_country_relation_table.insert().values(show_id=item_id, production_country_id=pc.id))

    def get_max_id(self, session: Session, model: Type[Any]) -> int:
        """
        Retrieves the maximum ID value for a given model from the database.

        Parameters:
        -----------
        session : Session
            The database session.
        model : Type[Any]
            The model class to query.

        Returns:
        --------
        int
            The maximum ID value.
        """
        max_id = session.query(func.max(model.id)).scalar()
        return max_id

    def to_dict(self, obj: Any) -> Dict[str, Any]:
        """
        Converts a SQLAlchemy model instance to a dictionary.

        Parameters:
        -----------
        obj : Any
            The SQLAlchemy model instance.

        Returns:
        --------
        Dict[str, Any]
            A dictionary representation of the model instance.
        """
        return {column.name: getattr(obj, column.name) for column in obj.__table__.columns}
