"""
Movie database management package.

This package provides functionality to initialize a movie database, add movies and actors,
search for movies, display information, and more.

Modules:
    db_init: Contains database initialization functions.
    data_insertion: Handles adding movies and actors.
    data_display: Provides functions to display movie, actor, and genre data.
    search: Handles searching for movies by keyword and pagination.
    utils: Contains utility functions for UUID generation and movie age calculation.
"""

from .db_init import init_database
from .data_insertion import add_movie, add_actor
from .data_display import (
    show_entire_library,
    show_unique_genres,
    count_movies_by_genre,
    avg_actor_age_in_genre,
    list_everything,
    list_movies_and_age
)
from .search import find_movie_by_keyword, show_movies_page_by_page
from .utils import create_uuid, movie_age

__all__ = [
    'add_actor', 'add_movie', 'avg_actor_age_in_genre', 'count_movies_by_genre',
    'create_uuid', 'find_movie_by_keyword', 'init_database', 'list_everything',
    'list_movies_and_age', 'movie_age', 'show_entire_library',
    'show_movies_page_by_page', 'show_unique_genres'
]
