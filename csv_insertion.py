import pandas as pd
from src.DataHandler import CsvDataHandler
from typing import List,Dict,Tuple
from src.database.Models import Base
from sqlalchemy.engine import Engine
from src.database.PostgresConnection import PostgresConnection
from src.database.DatabaseManager import DatabaseTableManager

def create_joined_df(title_dh: CsvDataHandler, best_netflix_df: pd.DataFrame, best_by_year_netflix_df: pd.DataFrame, col_to_drop: List[str], col_to_rename: Dict[str,str]):
    raw_credits_best_netflix_df = title_dh.joining_dfs(best_netflix_df,'title')
    raw_credits_best_netflix_dh: CsvDataHandler = CsvDataHandler(df=raw_credits_best_netflix_df)
    raw_credits_best_years_netflix_df = raw_credits_best_netflix_dh.joining_dfs(best_by_year_netflix_df,'title')
    raw_credits_best_years_netflix_dh: CsvDataHandler = CsvDataHandler(df=raw_credits_best_years_netflix_df)
    raw_credits_best_years_netflix_df.replace('', pd.NA, inplace=True)
    raw_credits_best_years_netflix_dh.change_values_to_flag('release_year')
    raw_credits_best_years_netflix_dh.drop_columns(col_to_drop)
    raw_credits_best_years_netflix_dh.rename_columns(col_to_rename)
    return raw_credits_best_years_netflix_df

def create_many_to_many_reliationship_df(joined_dh: CsvDataHandler, cols:List[str]) -> Tuple[pd.Series,pd.DataFrame]:
    unique_values = joined_dh.extract_unique_values(cols[1])
    joined_dh.map_values_to_indices(cols[1],unique_values)
    df = joined_dh.create_many_to_many_reliationship_df(cols)
    return (unique_values,df)

def from_series_to_df(series:pd.Series, col_name:str) -> pd.DataFrame:
    return pd.DataFrame({'id':range(1,len(series)+1), col_name:list(series)})

if __name__ == "__main__":
    postgres_connection: PostgresConnection = PostgresConnection()
    engine: Engine = postgres_connection.get_engine()

    Base.metadata.create_all(engine)

    file_paths = {
        'best_movie_by_year_netflix': "./Best Movie by Year Netflix.csv",
        'best_movies_netflix'       : "./Best Movies Netflix.csv",
        'best_show_by_year_netflix' : "./Best Show by Year Netflix.csv",
        'best_shows_netflix'        : "./Best Movie by Year Netflix.csv",
        'raw_credits'               : "./raw_credits.csv",
        'raw_titles'                : "./raw_titles.csv",
    }
    best_movies_by_year_netflix_dh: CsvDataHandler = CsvDataHandler(file_paths['best_movie_by_year_netflix'])
    best_movies_netflix_dh: CsvDataHandler = CsvDataHandler(file_paths['best_movies_netflix'])
    best_show_by_year_netflix_dh: CsvDataHandler = CsvDataHandler(file_paths['best_show_by_year_netflix'])
    best_shows_netflix_dh: CsvDataHandler = CsvDataHandler(file_paths['best_shows_netflix'])
    raw_credits_dh: CsvDataHandler = CsvDataHandler(file_paths['raw_credits'])
    raw_titles_dh: CsvDataHandler = CsvDataHandler(file_paths['raw_titles'])

    raw_titles_df: pd.DataFrame = raw_titles_dh.read_data_to_df()
    movies_df,shows_df = raw_titles_dh.seperate_dfs_by_column_values('type',['MOVIE','SHOW'])

    movies_dh: CsvDataHandler = CsvDataHandler(df=movies_df)
    shows_dh: CsvDataHandler = CsvDataHandler(df=shows_df)

    best_movies_netflix_df: pd.DataFrame = best_movies_netflix_dh.read_data_to_df()
    best_movies_netflix_dh.columns_to_lowercase()

    best_movies_by_year_netflix_df: pd.DataFrame = best_movies_by_year_netflix_dh.read_data_to_df()
    best_movies_by_year_netflix_dh.columns_to_lowercase()

    best_shows_netflix_df: pd.DataFrame = best_shows_netflix_dh.read_data_to_df()
    best_shows_netflix_dh.columns_to_lowercase()

    best_show_by_year_netflix_df: pd.DataFrame = best_show_by_year_netflix_dh.read_data_to_df()
    best_show_by_year_netflix_dh.columns_to_lowercase()

    raw_credits_df: pd.DataFrame = raw_credits_dh.read_data_to_df()

    movies_df_col_to_rename={
        'main_genre_y':'main_genre',
        'main_production_y':'main_production',
        'release_year_y':'release_year',
        'release_year':'is_movie_best_in_release_year',
    }
    movies_df_columns_to_drop = ['index_x','index_y','release_year_x','score_x','main_genre_x','main_production_x',
                                                        'number_of_votes','score_y','seasons','index']

    joined_movie_df = create_joined_df(movies_dh,best_movies_netflix_df,best_movies_by_year_netflix_df,
                                    movies_df_columns_to_drop,movies_df_col_to_rename)
    joined_movie_dh: CsvDataHandler = CsvDataHandler(df=joined_movie_df)
    unique_movie_genres, movie_id_genres_df = create_many_to_many_reliationship_df(joined_movie_dh,['id','genres'])
    unique_movie_genres_df = from_series_to_df(unique_movie_genres,'genre')

    movie_id_genres_df.rename(columns={
        'id':"movie_id",
        'genres': 'genre_id'
    },inplace=True)

    unique_production_countries, movie_id_production_countries_df = create_many_to_many_reliationship_df(joined_movie_dh,['id','production_countries'])
    unique_production_countries_df = from_series_to_df(unique_production_countries,'production_country')

    movie_id_production_countries_df.rename(columns={
        'id':"movie_id",
        'production_countries': 'production_country_id'
    },inplace=True)

    joined_movie_dh.drop_columns(['genres','production_countries'])
    [movies_df_columns_to_drop.remove(x) for x in ['seasons','number_of_votes','release_year_x']]
    movies_df_columns_to_drop.append("release_year_y")
    del(movies_df_col_to_rename['release_year_y'])
    movies_df_col_to_rename['release_year_x'] = 'release_year'

    joined_show_df: pd.DataFrame = create_joined_df(shows_dh,best_shows_netflix_df,best_show_by_year_netflix_df,movies_df_columns_to_drop,movies_df_col_to_rename)
    joined_show_dh: CsvDataHandler = CsvDataHandler(df=joined_show_df)

    unique_shows_genres, show_id_genres_df = create_many_to_many_reliationship_df(joined_show_dh,['id','genres'])
    unique_shows_production_countries ,show_id_production_countries_df = create_many_to_many_reliationship_df(joined_show_dh,['id','production_countries'])
    unique_shows_genres_df = from_series_to_df(unique_shows_genres,'genre')
    unique_shows_production_countries_df = from_series_to_df(unique_shows_production_countries,'production_country')
    show_id_genres_df.rename(columns={
        'id':"show_id",
        'genres': 'genre_id'
    },inplace=True)
    show_id_production_countries_df.rename(columns={
        'id':"show_id",
        'production_countries': 'production_country_id'
    },inplace=True)

    joined_show_dh.drop_columns(['genres','production_countries'])

    raw_credits_dh.rename_columns({
        'id'   : 'movie_id',
        'index': 'id'
    })

    unqiue_credits_name, credits_movie_id_name_df = create_many_to_many_reliationship_df(raw_credits_dh,['movie_id','name'])
    unqiue_credits_role, credits_movie_id_role_df = create_many_to_many_reliationship_df(raw_credits_dh,['movie_id','role'])
    unqiue_credits_name_df = from_series_to_df(unqiue_credits_name,'name')
    unqiue_credits_role_df = from_series_to_df(unqiue_credits_role,'role')
    credits_many_to_many_df = pd.concat([credits_movie_id_name_df, credits_movie_id_role_df], axis=1)
    credits_many_to_many_df = credits_many_to_many_df.loc[:, ~credits_many_to_many_df.columns.duplicated()].dropna()

    for table_tuple in [(joined_movie_df,'movie'),(unique_movie_genres_df,'movie_genre'),(movie_id_genres_df,'movie_genre_link'),
                  (unique_production_countries_df,'movie_production_country'),(movie_id_production_countries_df,'movie_production_country_link'),
                  (joined_show_df,'show'),(unique_shows_genres_df,'show_genre'),(unique_shows_production_countries_df,'show_production_country'),
                  (show_id_genres_df,'show_genre_link'),(show_id_production_countries_df,'show_production_country_link')]:
        dbt: DatabaseTableManager = DatabaseTableManager(engine,table_tuple[0],table_tuple[1])
        dbt.insert_df_into_database()

    raw_credits_dh.drop_columns(['name','role','person_id','movie_id'])
    raw_credits_df.dropna(inplace=True)
    raw_credit_dbt: DatabaseTableManager = DatabaseTableManager(engine,raw_credits_df,'credit')
    raw_credit_dbt.insert_df_into_database()

    credits_many_to_many_copy_df = credits_many_to_many_df.copy()
    movie_actors_credits_dh: CsvDataHandler = CsvDataHandler(df=credits_many_to_many_df)
    movie_actors_credits_dh.rename_columns({
        'movie_id':'id'
    })
    movie_actors_df = movie_actors_credits_dh.joining_dfs(joined_movie_df,'id','inner')

    show_actors_credits_dh: CsvDataHandler = CsvDataHandler(df=credits_many_to_many_copy_df)
    show_actors_credits_dh.rename_columns({
        'movie_id':'id'
    })
    show_actors_df = show_actors_credits_dh.joining_dfs(joined_show_df,'id','inner')

    movie_actors_dh: CsvDataHandler = CsvDataHandler(df=movie_actors_df)
    show_actors_dh: CsvDataHandler = CsvDataHandler(df=show_actors_df)
    movie_actors_dh.rename_columns({
        'id':'movie_id'
    })
    show_actors_dh.rename_columns({
        'id':'show_id'
    })
    for table_tuple in [(unqiue_credits_name_df,'actor'),(unqiue_credits_role_df,'role'),(movie_actors_df[['movie_id','name','role']],'movie_actor'),
                        (show_actors_df[['show_id','name','role']],'show_actor')]:
        dbt: DatabaseTableManager = DatabaseTableManager(engine,table_tuple[0],table_tuple[1])
        dbt.insert_df_into_database()