"""
This module provides functions for interacting with an SQLite database for storing
and managing movie and actor information. It includes the ability to initialize
the database, add records, display movies by various criteria, and perform
calculations related to genres and actor ages.

Functions:
- init_database: Initialize the SQLite database with a schema from a SQL script.
- add_movie: Add a new movie record to the database.
- add_actor: Add a new actor record to the database.
- show_entire_library: Display all movies and associated actors.
- show_unique_genres: Display a list of all unique movie genres.
- count_movies_by_genre: Display the number of movies for each genre.
- avg_age_in_genre: Calculate the average age of actors in each genre.
- movie_by_keyword: Search and display movies by a keyword in the title.
- movies_page_by_page: Paginate and display movies in pages.
- list_everything: Display a combined list of all movies and actors.
- list_movie_age: Display a list of movies and their ages.

Utility functions:
- create_uuid: Generate a new UUID string.
- movie_age: Calculate the age of a movie based on its release year.
"""

import sqlite3
import uuid
import math
from datetime import date

__all__ = ['init_database', 'add_movie', 'add_actor', 'show_entire_library',
           'show_unique_genres', 'count_movies_by_genre', 'avg_actor_age_in_genre',
           'find_movie_by_keyword', 'show_movies_page_by_page', 'list_everything',
           'list_movies_and_age', 'create_uuid', 'movie_age']


# ---- Utility functions ----

def create_uuid():
    """
    Generate a new UUID.

    :return: UUID string.
    :rtype: str
    """
    return str(uuid.uuid4())


def movie_age(year):
    """
    Calculate the age of a movie based on its release year.

    :param year: Release year of the movie.
    :type year: int
    :return: Age of the movie in years.
    :rtype: int
    """
    return date.today().year - year


def add_movie_cast(movie_id, actor_id):
    try:
        sqlite_connection = sqlite3.connect('movie_database.db')
        cursor = sqlite_connection.cursor()

        sqlite_add_movie_cast = '''
            INSERT OR IGNORE INTO movie_cast
            (movie_cast_id, movie_id, actor_id)
            VALUES (?, ?, ?);
        '''

        movie_cast_id = create_uuid()
        data = (movie_cast_id, movie_id, actor_id)
        cursor.execute(sqlite_add_movie_cast, data)

        sqlite_connection.commit()
        cursor.close()

    except sqlite3.Error as error:
        print("Error working with SQLite", error)

    finally:
        if sqlite_connection:
            sqlite_connection.close()


# ---- Database Initialization ----

def init_database():
    """
    Initialize the SQLite database using a SQL script file.
    Creates a function for generating UUIDs within SQL queries.

    :raises sqlite3.Error: If any error occurs during database interaction.
    """
    try:
        sqlite_connection = sqlite3.connect('movie_database.db')
        cursor = sqlite_connection.cursor()

        with open("movie_database_init.sql", 'r', encoding='utf-8') as script_file:
            init_script = script_file.read()

        sqlite_connection.create_function("uuid", 0, create_uuid)
        cursor.executescript(init_script)

        sqlite_connection.commit()
        cursor.close()

    except sqlite3.Error as error:
        print("Error working with SQLite", error)

    finally:
        if sqlite_connection:
            sqlite_connection.close()


# ---- Data Insertion Functions ----

def add_movie():
    """
    Add a new movie record to the database.

    :raises sqlite3.Error: If any error occurs during database interaction.
    """
    try:
        print("\nAdding movie", end='')
        sqlite_connection = sqlite3.connect('movie_database.db')
        cursor = sqlite_connection.cursor()

        sqlite_insert_movie = '''
            INSERT OR IGNORE INTO movies
            (movie_id, title, release_year, genre)
            VALUES (?, ?, ?, ?);
        '''

        movie_id = create_uuid()

        print("\nEnter movie title:")
        while True:
            title = input(">>> ")
            if not title:
                print("\nInvalid input. Title cannot be empty.")
                continue
            break

        print("\nEnter movie release year:")
        while True:
            year = input(">>> ")
            if not year:
                print("\nInvalid input. Please try again")
                continue
            try:
                year = int(year)
                if year <= 0:
                    raise ValueError
            except ValueError:
                print("\nInvalid input. Please enter a valid release year:")
                continue
            break

        print("\nEnter movie genre:")
        while True:
            genre = input(">>> ")
            if not genre:
                print("\nInvalid input. Genre cannot be empty.")
                continue
            break

        data = (movie_id, title, year, genre)
        cursor.execute(sqlite_insert_movie, data)
        print(f'\nMovie "{title}" was added to the database.')

        sqlite_connection.commit()
        cursor.close()

        print("Would you like to add cast to this movie?")
        print("1. Add a new actor/actress")
        print("2. Add an existing actor/actress")
        print("0. Proceed without adding cast")

        while True:
            actor_input = input(">>> ")
            if not actor_input:
                print("\nInvalid input. Please try again")
                continue
            try:
                actor_input = int(actor_input)
                if actor_input not in (1, 2, 0):
                    raise ValueError
            except ValueError:
                print("\nInvalid input. Please select one of the options:")
                continue
            break

        if actor_input == 1:
            actor_name, actor_birth_year = add_actor()
        elif actor_input == 2:
            try:
                sqlite_connection = sqlite3.connect('movie_database.db')
                cursor = sqlite_connection.cursor()

                sqlite_select_all_actor = '''
                    SELECT rowid, actor_id, name
                    FROM actors;
                '''

                cursor.execute(sqlite_select_all_actor)
                list_of_actors = cursor.fetchall()
                print("\nAvailable actors:")

                for actor in list_of_actors:
                    print(f"{actor[0]}. {actor[2]}")

                print(f"\nSelect an actor/actress to add to the cast: ")

                while True:
                    actor_no_input = input(">>> ")
                    if not actor_input:
                        print("\nInvalid input. Please try again")
                        continue
                    try:
                        actor_no_input = int(actor_no_input)
                        if actor_no_input not in range(1, len(list_of_actors)+1):
                            raise ValueError
                    except ValueError:
                        print("\nInvalid input. Please select one of the options:")
                        continue
                    break

                sqlite_insert_an_actor = '''
                    INSERT OR IGNORE INTO movie_cast
                    (movie_cast_id, movie_id, actor_id)
                    VALUES (?, ?, ?);
                '''

                selected_actor = list_of_actors[actor_no_input - 1][1]
                cast_insert = (create_uuid(), movie_id, selected_actor)
                cursor.execute(sqlite_insert_an_actor, cast_insert)

                selected_actor_name = list_of_actors[actor_no_input - 1][2]
                print(f"{selected_actor_name} was added to the cast of {title}")

                sqlite_connection.commit()
                cursor.close()

            except sqlite3.Error as error:
                print("Error working with SQLite", error)

            finally:
                if sqlite_connection:
                    sqlite_connection.close()

    except sqlite3.Error as error:
        print("Error working with SQLite", error)

    finally:
        if sqlite_connection:
            sqlite_connection.close()


def add_actor():
    """
    Add a new actor record to the database.

    :raises sqlite3.Error: If any error occurs during database interaction.
    """
    try:
        print("\nAdding actor.", end='')
        sqlite_connection = sqlite3.connect('movie_database.db')
        cursor = sqlite_connection.cursor()

        sqlite_insert_actor = '''
            INSERT OR IGNORE INTO actors
            (actor_id, name, birth_year)
            VALUES (?, ?, ?);
        '''

        actor_id = create_uuid()

        print("\nEnter actor's / actresses' full name:")
        while True:
            name = input(">>> ")
            if not name:
                print("\nInvalid input. Name cannot be empty.")
                continue
            break

        print("\nEnter actor's / actresses' birth year:")
        while True:
            year = input(">>> ")
            if not year:
                print("\nInvalid input. Please try again")
                continue
            try:
                year = int(year)
                if year <= 0:
                    raise ValueError
            except ValueError:
                print("\nInvalid input. Please enter a valid birth year:")
                continue
            break

        data = (actor_id, name, year)
        cursor.execute(sqlite_insert_actor, data)
        print(f"\nActor/actress {name} was added to the database.")

        sqlite_connection.commit()
        cursor.close()

        return (name, year)

    except sqlite3.Error as error:
        print("Error working with SQLite", error)
        return None

    finally:
        if sqlite_connection:
            sqlite_connection.close()


# ---- Data Display Functions ----

def show_entire_library():
    """
    Display all movies and associated actors from the database.

    :raises sqlite3.Error: If any error occurs during database interaction.
    """
    try:
        print("\nList of all movies with the cast:")
        sqlite_connection = sqlite3.connect('movie_database.db')
        cursor = sqlite_connection.cursor()

        sqlite_select_entire_library = '''
            SELECT m.title, a.name
            FROM movie_cast mc
            INNER JOIN movies m on m.movie_id = mc.movie_id
            INNER JOIN actors a on a.actor_id = mc.actor_id
            ORDER BY 1, 2;
        '''

        cursor.execute(sqlite_select_entire_library)
        movie_library = cursor.fetchall()

        for entry in movie_library:
            print(f"Movie: {entry[0]}. Actor: {entry[1]}")

        sqlite_connection.commit()
        cursor.close()

    except sqlite3.Error as error:
        print("Error working with SQLite", error)

    finally:
        if sqlite_connection:
            sqlite_connection.close()


def show_unique_genres():
    """
    Display a list of all unique movie genres from the database.

    :raises sqlite3.Error: If any error occurs during database interaction.
    """
    try:
        print("\nList of unique genres:")
        sqlite_connection = sqlite3.connect('movie_database.db')
        cursor = sqlite_connection.cursor()

        sqlite_select_unique_genres = '''
            SELECT DISTINCT genre
            FROM movies
            ORDER BY genre;
        '''

        cursor.execute(sqlite_select_unique_genres)
        genre_list = cursor.fetchall()

        print("Genres:")
        for genre in genre_list:
            print(f"- {genre[0]}")

        sqlite_connection.commit()
        cursor.close()

    except sqlite3.Error as error:
        print("Error working with SQLite", error)

    finally:
        if sqlite_connection:
            sqlite_connection.close()


def count_movies_by_genre():
    """
    Display the number of movies in each genre.

    :raises sqlite3.Error: If any error occurs during database interaction.
    """
    try:
        print("\nNumber of movies by genre:")
        sqlite_connection = sqlite3.connect('movie_database.db')
        cursor = sqlite_connection.cursor()

        sqlite_count_movies_by_genre = '''
            SELECT genre, count(movie_id)
            FROM movies
            GROUP BY genre
            ORDER BY genre;
        '''

        cursor.execute(sqlite_count_movies_by_genre)
        movies_by_genre = cursor.fetchall()

        for number, genre in enumerate(movies_by_genre, 1):
            print(f"{number}. {genre[0]}: {genre[1]}")

        sqlite_connection.commit()
        cursor.close()

    except sqlite3.Error as error:
        print("Error working with SQLite", error)

    finally:
        if sqlite_connection:
            sqlite_connection.close()


def avg_actor_age_in_genre():
    """
    Calculate and display the average age of actors in each genre.

    :raises sqlite3.Error: If any error occurs during database interaction.
    """
    try:
        print("\nAverage cast age in genre:")
        sqlite_connection = sqlite3.connect('movie_database.db')
        cursor = sqlite_connection.cursor()

        sqlite_avg_actor_age_in_genre = '''
            SELECT m.genre, AVG(DATE('now') - a.birth_year)
            FROM movie_cast mc
            INNER JOIN movies m on m.movie_id = mc.movie_id
            INNER JOIN actors a on a.actor_id = mc.actor_id
            GROUP BY genre
            ORDER BY genre;
        '''

        cursor.execute(sqlite_avg_actor_age_in_genre)
        avg_age_in_genre = cursor.fetchall()

        for number, entry in enumerate(avg_age_in_genre, 1):
            print(f"{number}. Genre: {(entry[0].lower())}, "
                  f"average cast age: {round(entry[1])}")

        sqlite_connection.commit()
        cursor.close()

    except sqlite3.Error as error:
        print("Error working with SQLite", error)

    finally:
        if sqlite_connection:
            sqlite_connection.close()


# ---- Movie Search Functions ----

def find_movie_by_keyword():
    """
    Search for movies by a keyword in the title and display the results.

    Prompts the user for input to enter a keyword for the search.

    :raises sqlite3.Error: If any error occurs during database interaction.
    """
    try:
        print("\nSearching for a movie by keyword:")
        sqlite_connection = sqlite3.connect('movie_database.db')
        cursor = sqlite_connection.cursor()

        movies_by_keyword = '''
            SELECT title, release_year
            FROM movies
            WHERE title LIKE ?;
        '''

        print("\nEnter keyword: ")
        keyword = input(">>> ")
        keyword = f"%{keyword}%"
        cursor.execute(movies_by_keyword, (keyword,))
        movies_by_keyword_list = cursor.fetchall()

        if movies_by_keyword_list:
            print("\nFound movies:")
            for number, movie in enumerate(movies_by_keyword_list, 1):
                print(f"{number}. {movie[0]} ({movie[1]})")
        else:
            print("No movies found with that keyword.")

        sqlite_connection.commit()
        cursor.close()

    except sqlite3.Error as error:
        print("Error working with SQLite", error)

    finally:
        if sqlite_connection:
            sqlite_connection.close()


def show_movies_page_by_page():
    """
    Display movies from the database in a paginated format.

    Prompts the user for input to determine the number of movies per page
    and navigates through pages.

    :raises sqlite3.Error: If any error occurs during database interaction.
    """
    try:
        print("\nList of movies page by page:")
        sqlite_connection = sqlite3.connect('movie_database.db')
        cursor = sqlite_connection.cursor()

        sqlite_select_total_pages = '''
            SELECT CAST(COUNT(movie_id) AS REAL) / ?
            FROM movies
        '''

        print("Select how many movies to show by page:")
        while True:
            movies_by_page = input(">>> ")
            try :
                movies_by_page = int(movies_by_page)
                if movies_by_page <= 0:
                    print("\nInvalid input. Please enter a number greater than 0:")
                    continue
            except ValueError:
                print("\nInvalid input. Please enter a valid number:")
                continue
            break

        cursor.execute(sqlite_select_total_pages, (movies_by_page,))
        total_pages = math.ceil(cursor.fetchone()[0])

        sqlite_select_page_with_movies = '''
            SELECT title
            FROM movies
            ORDER BY title
            LIMIT ?
            OFFSET ?;
        '''

        offset = 0
        page_counter = 1
        movie_index = 1

        while True:
            cursor.execute(sqlite_select_page_with_movies, (movies_by_page, offset))
            output = cursor.fetchall()

            print(f"\nPage {page_counter} of {total_pages}")
            for number, movie in enumerate(output, movie_index):
                print(f"{number}. {movie[0]}")

            if page_counter == 1:
                print('For next page - enter "n", to exit - any other key: ')
            elif page_counter < total_pages:
                print('For next page - enter "n", for previous page - enter "p", '
                      'to exit - any other key: ')
            else:
                print('For previous page - enter "p", to exit - any other key: ')

            action = input(">>> ")

            if action == 'n':
                page_counter += 1
                movie_index += movies_by_page
                offset += movies_by_page
            elif action == 'p':
                page_counter -= 1
                movie_index -= movies_by_page
                offset -= movies_by_page
            else:
                break

        sqlite_connection.commit()
        cursor.close()

    except sqlite3.Error as error:
        print("Error working with SQLite", error)

    finally:
        if sqlite_connection:
            sqlite_connection.close()


def list_everything():
    """
    Display a combined list of all movies and actors from the database.

    :raises sqlite3.Error: If any error occurs during database interaction.
    """
    try:
        print("\nAll actors and movies:")
        sqlite_connection = sqlite3.connect('movie_database.db')
        cursor = sqlite_connection.cursor()

        select_list_of_everything = '''
            SELECT title, "Movie" AS Type
            FROM movies
            UNION
            SELECT name, "Actor" AS Type
            FROM actors
            ORDER BY 2, 1;
        '''

        cursor.execute(select_list_of_everything)
        list_of_everything = cursor.fetchall()

        if list_of_everything:
            for number, item in enumerate(list_of_everything, 1):
                print(f"{number}. {item[0]} ({item[1]})")
        else:
            print("No actors or movies found.")

        sqlite_connection.commit()
        cursor.close()

    except sqlite3.Error as error:
        print("Error working with SQLite", error)

    finally:
        if sqlite_connection:
            sqlite_connection.close()


def list_movies_and_age():
    """
    Display a list of movies and their ages.

    Uses the movie_age function to calculate the age of each movie.

    :raises sqlite3.Error: If any error occurs during database interaction.
    """
    try:
        print("\nMovies and their age:")
        sqlite_connection = sqlite3.connect('movie_database.db')
        cursor = sqlite_connection.cursor()

        sqlite_connection.create_function("movie_age", 1, movie_age)

        select_movies_and_age = '''
            SELECT title, movie_age(release_year)
            FROM movies
            ORDER BY title;
        '''

        cursor.execute(select_movies_and_age)
        list_of_movies_and_age = cursor.fetchall()

        if list_of_movies_and_age:
            for number, item in enumerate(list_of_movies_and_age, 1):
                print(f"{number}. {item[0]} ({item[1]} years)")
        else:
            print("No movies found.")

        sqlite_connection.commit()
        cursor.close()

    except sqlite3.Error as error:
        print("Error working with SQLite", error)

    finally:
        if sqlite_connection:
            sqlite_connection.close()
