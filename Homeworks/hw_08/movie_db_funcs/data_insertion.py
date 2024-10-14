"""
Module for managing movies and actors in a SQLite movie database.

This module provides functionality to add movies, actors, and cast members
to a movie database, using UUIDs for unique identification.

Requires:
    sqlite3: A built-in Python module for working with SQLite databases.
    .utils: A custom utility module containing the create_uuid function.

Functions:
    add_movie_cast: Add an actor to a movie's cast.
    add_actor: Add a new actor to the database.
    add_movie: Add a new movie to the database and optionally add cast members.
"""

from .utils import create_uuid
import sqlite3


# ---- Add actor to movie cast ----
def add_movie_cast(movie_id, actor_id):
    """
    Add an actor to a movie's cast.

    :param movie_id: The ID of the movie.
    :type movie_id: str
    :param actor_id: The ID of the actor.
    :type actor_id: str
    :raises sqlite3.Error: If any error occurs during database interaction.
    """
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


# ---- Add new actor to the database ----
def add_actor():
    """
    Add a new actor record to the database.

    Prompts the user for input to gather actor information.

    :raises sqlite3.Error: If any error occurs during database interaction.
    :return: Tuple containing the actor's name and birth year.
    :rtype: tuple
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

        print("\nEnter actor's / actress' full name:")
        while True:
            name = input(">>> ")
            if not name:
                print("\nInvalid input. Name cannot be empty.")
                continue
            break

        print("\nEnter actor's / actress' birth year:")
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

        return name, year

    except sqlite3.Error as error:
        print("Error working with SQLite", error)
        return None

    finally:
        if sqlite_connection:
            sqlite_connection.close()


# ---- Add new movie to the database ----
def add_movie():
    """
    Add a new movie record to the database.

    Prompts the user for input to gather information about the movie.

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

        # ---- Add cast to movie ----
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
            actor = add_actor()
            actor_name = actor[0]
            print(f"\n{actor_name} was added to the cast of {title}")

        elif actor_input == 2:
            # Code block for adding existing actor
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
                        if actor_no_input not in range(1, len(list_of_actors) + 1):
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
                print(f"\n{selected_actor_name} was added to the cast of {title}")

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
