from src.database.PostgresConnection import PostgresConnection
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import Engine
from typing import Generator

# Create a PostgresConnection instance
pc: PostgresConnection = PostgresConnection()

# Get the SQLAlchemy engine from the PostgresConnection instance
engine: Engine = pc.get_engine()

# Configure the sessionmaker with the engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Generator[Session, None, None]:
    """
    Provides a database session for use in a context where it will be automatically closed after use.
    
    Yields:
    -------
    Generator[Session, None, None]
        A SQLAlchemy Session object.
    """
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
