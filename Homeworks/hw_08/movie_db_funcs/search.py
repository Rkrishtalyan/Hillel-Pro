"""
Module for interacting with a movie database using SQLite.

This module provides functions to search for movies by a keyword and
display movies in a paginated format from an SQLite database.

Requires:
    sqlite3: A built-in Python module for working with SQLite databases.
    math: A built-in Python module for mathematical operations, used for
    calculating the number of pages in pagination.

Functions:
    find_movie_by_keyword: Search for movies by a keyword in the title.
    show_movies_page_by_page: Display movies in a paginated format.
"""

import sqlite3
import math


# ---- Find movie by keyword ----
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


# ---- Paginate movies display ----
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
            try:
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
