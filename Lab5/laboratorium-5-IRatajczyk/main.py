import numpy as np
import pickle

import psycopg2 as pg
import pandas.io.sql as psql
import pandas as pd

from typing import Union, List, Tuple

connection = pg.connect(host='pgsql-196447.vipserv.org', port=5432, dbname='wbauer_adb', user='wbauer_adb',
                        password='adb2020');


def film_in_category(category: Union[int, str]) -> pd.DataFrame:
    ''' Funkcja zwracająca wynik zapytania do bazy o tytuł filmu, język, oraz kategorię dla zadanego:
        - id: jeżeli categry jest int
        - name: jeżeli category jest str, dokładnie taki jak podana wartość
    Przykład wynikowej tabeli:
    |   |title          |languge    |category|
    |0	|Amadeus Holy	|English	|Action|
    
    Tabela wynikowa ma być posortowana po tylule filmu i języku.
    
    Jeżeli warunki wejściowe nie są spełnione to funkcja powinna zwracać wartość None.
    
    Parameters:
    category (int,str): wartość kategorii po id (jeżeli typ int) lub nazwie (jeżeli typ str)  dla którego wykonujemy zapytanie
    
    Returns:
    pd.DataFrame: DataFrame zawierający wyniki zapytania
    '''
    if isinstance(category, int):
        sql = f"""SELECT f.title AS title, l.name AS languge, c.name AS category
                    FROM category c
                    JOIN film_category fc USING(category_id)
                    JOIN film f USING(film_id)
                    JOIN language l USING(language_id)
                    WHERE c.category_id = {category} 
                    ORDER BY f.title, l.name
        """
        return pd.read_sql(sql, con=connection)
    elif isinstance(category, str):
        sql = f"""SELECT f.title AS title, l.name AS languge, c.name AS category
                    FROM category c
                    JOIN film_category fc USING(category_id)
                    JOIN film f USING(film_id)
                    JOIN language l USING(language_id)
                    WHERE c.name LIKE '{category}'
                    ORDER BY f.title, l.name
        """
        return pd.read_sql(sql, con=connection)
    else:
        return None


def film_in_category_case_insensitive(category: Union[int, str]) -> pd.DataFrame:
    ''' Funkcja zwracająca wynik zapytania do bazy o tytuł filmu, język, oraz kategorię dla zadanego:
        - id: jeżeli categry jest int
        - name: jeżeli category jest str
    Przykład wynikowej tabeli:
    |   |title          |languge    |category|
    |0	|Amadeus Holy	|English	|Action|
    
    Tabela wynikowa ma być posortowana po tylule filmu i języku.
    
    Jeżeli warunki wejściowe nie są spełnione to funkcja powinna zwracać wartość None.
    
    Parameters:
    category (int,str): wartość kategorii po id (jeżeli typ int) lub nazwie (jeżeli typ str)  dla którego wykonujemy zapytanie
    
    Returns:
    pd.DataFrame: DataFrame zawierający wyniki zapytania
    '''
    if isinstance(category, int):
        sql = f"""SELECT f.title AS title, l.name AS languge, c.name AS category
                    FROM category c
                    JOIN film_category fc USING(category_id)
                    JOIN film f USING(film_id)
                    JOIN language l USING(language_id)
                    WHERE c.category_id = {category} 
                    ORDER BY f.title, l.name
        """
        return pd.read_sql(sql, con=connection)
    elif isinstance(category, str):
        sql = f"""SELECT f.title AS title, l.name AS languge, c.name AS category
                    FROM category c
                    JOIN film_category fc USING(category_id)
                    JOIN film f USING(film_id)
                    JOIN language l USING(language_id)
                    WHERE c.name ILIKE '{category}'
                    ORDER BY f.title, l.name
        """
        return pd.read_sql(sql, con=connection)
    else:
        return None


def film_cast(title: str) -> pd.DataFrame:
    ''' Funkcja zwracająca wynik zapytania do bazy o obsadę filmu o dokładnie zadanym tytule.
    Przykład wynikowej tabeli:
    |   |first_name |last_name  |
    |0	|Greg       |Chaplin    | 
    
    Tabela wynikowa ma być posortowana po nazwisku i imieniu klienta.
    Jeżeli warunki wejściowe nie są spełnione to funkcja powinna zwracać wartość None.
        
    Parameters:
    title (int): wartość id kategorii dla którego wykonujemy zapytanie
    
    Returns:
    pd.DataFrame: DataFrame zawierający wyniki zapytania
    '''
    if isinstance(title, str):
        sql = f"""SELECT a.first_name AS first_name, a.last_name AS last_name
                            FROM film f
                            JOIN film_actor USING(film_id)
                            JOIN actor a USING(actor_id)
                            WHERE f.title LIKE '{title}'
                            ORDER BY a.last_name, a.first_name
                """
        return pd.read_sql(sql, con=connection)
    else:
        return None


def film_title_case_insensitive(words: list):
    ''' Funkcja zwracająca wynik zapytania do bazy o tytuły filmów zawierających conajmniej jedno z podanych słów z listy words.
    Przykład wynikowej tabeli:
    |   |title              |
    |0	|Crystal Breaking 	| 
    
    Tabela wynikowa ma być posortowana po nazwisku i imieniu klienta.

    Jeżeli warunki wejściowe nie są spełnione to funkcja powinna zwracać wartość None.
        
    Parameters:
    words(list): wartość minimalnej długości filmu
    
    Returns:
    pd.DataFrame: DataFrame zawierający wyniki zapytania
    '''
    if isinstance(words, list):
        X = "'"
        for elem in words:
            X += '^' + elem + ' | ' + elem + " | " + elem + "$|"
        X = X[:-1]
        X += "'"
        sql = f"""SELECT DISTINCT f.title
                            FROM film f
                            WHERE f.title ~* {X}
                """
        return pd.read_sql(sql, con=connection)
    else:
        return None
