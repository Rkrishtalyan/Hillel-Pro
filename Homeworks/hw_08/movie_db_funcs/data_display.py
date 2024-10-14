"""
Module for retrieving and displaying movie and actor information from a SQLite database.

This module provides functions to display various data related to movies, actors,
and genres from a movie database, including movie lists, cast lists, genre information,
and actor ages.

Requires:
    sqlite3: A built-in Python module for working with SQLite databases.
    .utils: A custom utility module containing the movie_age function.

Functions:
    show_entire_library: Display all movies and associated actors.
    show_unique_genres: Display a list of all unique movie genres.
    count_movies_by_genre: Display the number of movies in each genre.
    avg_actor_age_in_genre: Display the average age of actors in each genre.
    list_everything: Display a combined list of all movies and actors.
    list_movies_and_age: Display a list of movies along with their calculated age.
"""

import sqlite3
from .utils import movie_age


# ---- Display all movies and their cast ----
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


# ---- Display all unique movie genres ----
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


# ---- Count movies by genre ----
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


# ---- Calculate and display average actor age in each genre ----
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


# ---- Display a combined list of all movies and actors ----
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


# ---- Display movies and their ages ----
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
