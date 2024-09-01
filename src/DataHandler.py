import pandas as pd
from typing import Optional, Tuple, List, Dict

class CsvDataHandler:
    """
    A class to handle CSV data operations using pandas DataFrame.

    Attributes:
    -----------
    file_path : str
        The path to the CSV file.
    df : Optional[pd.DataFrame]
        The DataFrame to store the data.
    """

    def __init__(self, file_path: str = None, df: Optional[pd.DataFrame] = None) -> None:
        """
        Initializes the CsvDataHandler with a file path and an optional DataFrame.

        Parameters:
        -----------
        file_path : str, optional
            The path to the CSV file (default is None).
        df : Optional[pd.DataFrame], optional
            A pandas DataFrame (default is None).
        """
        self.file_path = file_path
        self.df: Optional[pd.DataFrame] = df

    def read_data_to_df(self) -> pd.DataFrame:
        """
        Reads data from a CSV file into a DataFrame.

        Returns:
        --------
        pd.DataFrame
            The DataFrame containing the data read from the CSV file.
        """
        self.df = pd.read_csv(self.file_path, header=0)
        return self.df
    
    def get_df(self) -> Optional[pd.DataFrame]:
        """
        Returns the current DataFrame.

        Returns:
        --------
        Optional[pd.DataFrame]
            The current DataFrame.
        """
        return self.df
    
    def seperate_dfs_by_column_values(self, seperation_column: str, col_values_to_seperate: List[str]) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Separates the DataFrame into two based on specified column values.

        Parameters:
        -----------
        seperation_column : str
            The column to use for separation.
        col_values_to_seperate : List[str]
            The values in the separation column to use for splitting the DataFrame.

        Returns:
        --------
        Tuple[pd.DataFrame, pd.DataFrame]
            Two DataFrames separated based on the specified column values.
        """
        return (self.df[self.df[seperation_column] == col_values_to_seperate[0]], self.df[self.df[seperation_column] == col_values_to_seperate[1]])
    
    def joining_dfs(self, df_to_merge: pd.DataFrame, join_on: str, join_method: str = 'left') -> pd.DataFrame:
        """
        Joins the current DataFrame with another DataFrame.

        Parameters:
        -----------
        df_to_merge : pd.DataFrame
            The DataFrame to merge with.
        join_on : str
            The column name to join on.
        join_method : str, optional
            The method of join (default is 'left').

        Returns:
        --------
        pd.DataFrame
            The joined DataFrame.
        """
        joined_df: pd.DataFrame = pd.merge(self.df, df_to_merge, on=join_on, how=join_method)
        return joined_df
    
    def drop_columns(self, columns_to_drop: str) -> None:
        """
        Drops specified columns from the DataFrame.

        Parameters:
        -----------
        columns_to_drop : str
            The columns to drop.
        """
        self.df.drop(columns=columns_to_drop, inplace=True, axis=1)
    
    def columns_to_lowercase(self) -> None:
        """
        Converts all column names in the DataFrame to lowercase.
        """
        self.df.columns = self.df.columns.str.lower()
    
    def rename_columns(self, col_dict_change: Dict[str, str]) -> None:
        """
        Renames columns in the DataFrame based on a dictionary mapping.

        Parameters:
        -----------
        col_dict_change : Dict[str, str]
            A dictionary mapping old column names to new column names.
        """
        self.df.rename(columns=col_dict_change, inplace=True)

    def change_column_type_to_string(self, col: str) -> None:
        """
        Changes the data type of a specified column to string.

        Parameters:
        -----------
        col : str
            The column to change to string type.
        """
        self.df[col] = self.df[col].astype(str)

    def change_values_to_flag(self, col: str) -> None:
        """
        Changes the values in a column to flags ('Y' or 'N') based on their presence.

        Parameters:
        -----------
        col : str
            The column to modify.
        """
        self.df[col] = self.df[col].apply(lambda x: 'N' if pd.isna(x) else 'Y')
    
    def extract_unique_values(self, column: str) -> pd.Series:
        """
        Extracts unique values from a specified column.

        Parameters:
        -----------
        column : str
            The column to extract unique values from.

        Returns:
        --------
        pd.Series
            A Series of unique values.
        """
        values_series = (
            self.df[column]
            .str.replace(r"[\[\]']", "", regex=True)
            .str.split(',')
            .explode()
            .dropna()
            .str.strip()
        )
        unique_values = pd.Series(values_series[values_series != ""].unique())
        return unique_values

    def map_values_to_indices(self, column: str, unique_values: pd.Series) -> None:
        """
        Maps values in a column to indices based on unique values.

        Parameters:
        -----------
        column : str
            The column to map.
        unique_values : pd.Series
            A Series of unique values to map to indices.
        """
        value_to_index = {value: index + 1 for index, value in unique_values.items()}
        
        self.df[column] = (
            self.df[column]
            .str.replace(r"[\[\]']", "", regex=True)
            .str.split(',')
            .apply(lambda values: [value_to_index[value.strip()] for value in values if value.strip() in value_to_index])
        )
        
    def create_many_to_many_reliationship_df(self, cols: List[str]) -> pd.DataFrame:
        """
        Creates a DataFrame representing a many-to-many relationship based on specified columns.

        Parameters:
        -----------
        cols : List[str]
            The columns to use for the many-to-many relationship.

        Returns:
        --------
        pd.DataFrame
            A DataFrame representing the many-to-many relationship.
        """
        many_to_many_df = pd.DataFrame({self.df[cols[0]].name: self.df[cols[0]], self.df[cols[1]].name: self.df[cols[1]]})
        many_to_many_df = many_to_many_df.explode(cols[1], ignore_index=True)
        return many_to_many_df
