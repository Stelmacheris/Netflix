import pandas as pd
from sqlalchemy.engine import Engine

class DatabaseTableManager:
    """
    A manager class for handling database table operations such as inserting a DataFrame into a table 
    and dropping specified columns from a table.
    
    Attributes:
        engine (Engine): The SQLAlchemy engine connected to the database.
        df (pd.DataFrame): The DataFrame to be inserted into the database.
        table_name (str): The name of the table in the database.
    """

    def __init__(self, engine: Engine, df: pd.DataFrame, table_name: str) -> None:
        """
        Initializes the DatabaseTableManager with a database engine, a DataFrame, and a table name.

        Args:
            engine (Engine): The SQLAlchemy engine connected to the database.
            df (pd.DataFrame): The DataFrame to be inserted into the database.
            table_name (str): The name of the table in the database.
        """
        self.engine = engine
        self.df = df
        self.table_name = table_name

    def insert_df_into_database(self) -> None:
        """
        Inserts the DataFrame into the specified table in the database.

        If the table already exists, the DataFrame will be appended to it.
        """
        self.df.to_sql(self.table_name, self.engine, if_exists='append',index=False)