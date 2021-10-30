import numpy as np
import pickle

import psycopg2 as pg
import pandas.io.sql as psql
import pandas as pd

from typing import Union, List, Tuple

connection = pg.connect(host='pgsql-196447.vipserv.org', port=5432, dbname='wbauer_adb', user='wbauer_adb',
                        password='adb2020');


def film_in_category(category_id: int) -> pd.DataFrame:
    ''' Funkcja zwracająca wynik zapytania do bazy o tytuł filmu, język, oraz kategorię dla zadanego id kategorii.
    Przykład wynikowej tabeli:
    |   |title          |languge    |category|
    |0	|Amadeus Holy	|English	|Action|
    
    Tabela wynikowa ma być posortowana po tylule filmu i języku.
    
    Jeżeli warunki wejściowe nie są spełnione to funkcja powinna zwracać wartość None.
    
    Parameters:
    category_id (int): wartość id kategorii dla którego wykonujemy zapytanie
    
    Returns:
    pd.DataFrame: DataFrame zawierający wyniki zapytania
    '''
    if isinstance(category_id, int) and category_id >= 0:
        sql = f'''SELECT f.title AS title, l.name AS languge, c.name AS category
                      FROM category c
                      JOIN film_category USING (category_id)
                      JOIN film f USING(film_id)
                      JOIN language l USING(language_id)
                      WHERE c.category_id = {category_id}
                      ORDER BY f.title, l.name'''

        df = pd.read_sql(sql, con=connection)
        return df
    else:
        return None


def number_films_in_category(category_id: int) -> pd.DataFrame:
    ''' Funkcja zwracająca wynik zapytania do bazy o ilość filmów w zadanej kategori przez id kategorii.
    Przykład wynikowej tabeli:
    |   |category   |count|
    |0	|Action 	|64	  | 
    
    Jeżeli warunki wejściowe nie są spełnione to funkcja powinna zwracać wartość None.
        
    Parameters:
    category_id (int): wartość id kategorii dla którego wykonujemy zapytanie
    
    Returns:
    pd.DataFrame: DataFrame zawierający wyniki zapytania
    '''
    if isinstance(category_id, int):
        sql = f'''SELECT c.name AS category, COUNT(c.name) AS count 
        FROM category c
        JOIN film_category USING(category_id) 
        WHERE category_id = {category_id}
        GROUP BY c.name'''

        df = pd.read_sql(sql, con=connection)
        return df
    else:
        return None


def number_film_by_length(min_length: Union[int, float] = 0, max_length: Union[int, float] = 1e6):
    ''' Funkcja zwracająca wynik zapytania do bazy o ilość filmów o dla poszczegulnych długości pomiędzy wartościami min_length a max_length.
    Przykład wynikowej tabeli:
    |   |length     |count|
    |0	|46 	    |64	  | 
    
    Jeżeli warunki wejściowe nie są spełnione to funkcja powinna zwracać wartość None.
        
    Parameters:
    min_length (int,float): wartość minimalnej długości filmu
    max_length (int,float): wartość maksymalnej długości filmu
    
    Returns:
    pd.DataFrame: DataFrame zawierający wyniki zapytania
    '''
    if (isinstance(min_length, int) or isinstance(min_length, float)) and (
            isinstance(max_length, int) or isinstance(max_length, float))\
            and min_length <= max_length:
        sql = f'''SELECT f.length AS length, COUNT(*)
        FROM film f
        WHERE f.length BETWEEN {min_length} AND {max_length}
        GROUP BY f.length
        '''

        df = pd.read_sql(sql, con=connection)
        return df
    else:
        return None


def client_from_city(city: str) -> pd.DataFrame:
    ''' Funkcja zwracająca wynik zapytania do bazy o listę klientów z zadanego miasta przez wartość city.
    Przykład wynikowej tabeli:
    |   |city	    |first_name	|last_name
    |0	|Athenai	|Linda	    |Williams
    
    Tabela wynikowa ma być posortowana po nazwisku i imieniu klienta.
    
    Jeżeli warunki wejściowe nie są spełnione to funkcja powinna zwracać wartość None.
        
    Parameters:
    city (str): nazwa miaste dla którego mamy sporządzić listę klientów
    
    Returns:
    pd.DataFrame: DataFrame zawierający wyniki zapytania
    '''

    if isinstance(city, str):
        sql = f'''SELECT c.city AS city, cu.first_name AS first_name, cu.last_name AS last_name 
        FROM customer cu 
        JOIN address USING(address_id) 
        JOIN city c USING(city_id) 
        WHERE c.city = '{city}'
        ORDER BY cu.last_name, cu.first_name'''

        df = pd.read_sql(sql, con=connection)
        return df
    else:
        return None


def avg_amount_by_length(length: Union[int, float]) -> pd.DataFrame:
    ''' Funkcja zwracająca wynik zapytania do bazy o średnią wartość wypożyczenia filmów dla zadanej długości length.
    Przykład wynikowej tabeli:
    |   |length |avg
    |0	|48	    |4.295389
    
    
    Jeżeli warunki wejściowe nie są spełnione to funkcja powinna zwracać wartość None.
        
    Parameters:
    length (int,float): długość filmu dla którego mamy pożyczyć średnią wartość wypożyczonych filmów
    
    Returns:
    pd.DataFrame: DataFrame zawierający wyniki zapytania
    '''
    if isinstance(length, int) or isinstance(length,float):
        sql = f'''
        SELECT  f.length AS length, AVG(p.amount) AS avg
        FROM film f
        JOIN inventory USING (film_id) 
        JOIN rental USING(inventory_id) 
        JOIN payment p USING(rental_id) 
        WHERE f.length = {length}
        GROUP BY f.length
        '''

        df = pd.read_sql(sql, con=connection)
        return df
    else:
        return None


def client_by_sum_length(sum_min: Union[int, float]) -> pd.DataFrame:
    ''' Funkcja zwracająca wynik zapytania do bazy o sumaryczny czas wypożyczonych filmów przez klientów powyżej zadanej wartości .
    Przykład wynikowej tabeli:
    |   |first_name |last_name  |sum
    |0  |Brian	    |Wyman  	|1265
    
    Tabela wynikowa powinna być posortowane według sumy, imienia i nazwiska klienta.
    Jeżeli warunki wejściowe nie są spełnione to funkcja powinna zwracać wartość None.
        
    Parameters:
    sum_min (int,float): minimalna wartość sumy długości wypożyczonych filmów którą musi spełniać klient
    
    Returns:
    pd.DataFrame: DataFrame zawierający wyniki zapytania
    '''
    if (isinstance(sum_min, int) or isinstance(sum_min, float)) and sum_min >= 0:
        sql = f'''
                SELECT cu.first_name AS first_name, cu.last_name AS last_name, SUM(f.length)
                FROM film f
                JOIN inventory USING (film_id) 
                JOIN rental USING(inventory_id) 
                JOIN customer cu USING(customer_id) 
                GROUP BY cu.last_name, cu.first_name
                HAVING SUM(f.length) > {sum_min}
                ORDER BY SUM(f.length), cu.last_name, cu.first_name '''

        df = pd.read_sql(sql, con=connection)
        return df
    else:
        return None


def category_statistic_length(name: str) -> pd.DataFrame:
    ''' Funkcja zwracająca wynik zapytania do bazy o statystykę długości filmów w kategorii o zadanej nazwie.
    Przykład wynikowej tabeli:
    |   |category   |avg    |sum    |min    |max
    |0	|Action 	|111.60 |7143   |47 	|185
    
    Jeżeli warunki wejściowe nie są spełnione to funkcja powinna zwracać wartość None.
        
    Parameters:
    name (str): Nazwa kategorii dla której ma zostać wypisana statystyka
    
    Returns:
    pd.DataFrame: DataFrame zawierający wyniki zapytania
    '''
    if isinstance(name, str):
        sql = f'''SELECT c.name AS category, AVG(f.length) AS avg, SUM(f.length) AS sum, MIN(f.length) AS min, MAX(f.length) AS max
                FROM film f
                JOIN film_category USING(film_id) 
                JOIN category c USING(category_id)
                WHERE c.name = '{name}'
                GROUP BY c.name
                '''

        df = pd.read_sql(sql, con=connection)
        return df
    else:
        return None
