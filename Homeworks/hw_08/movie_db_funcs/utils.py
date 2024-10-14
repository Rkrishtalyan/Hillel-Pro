"""
Utility module for generating UUIDs and calculating the age of movies.

This module provides utility functions to generate unique identifiers
(UUIDs) and calculate the age of a movie based on its release year.

Requires:
    uuid: A built-in Python module for generating universally unique identifiers.
    datetime: A built-in Python module for working with dates and times.

Functions:
    create_uuid: Generate a new UUID.
    movie_age: Calculate the age of a movie based on its release year.
"""

import uuid
from datetime import date


# ---- UUID generation ----
def create_uuid():
    """
    Generate a new UUID.

    :return: UUID string.
    :rtype: str
    """
    return str(uuid.uuid4())


# ---- Movie age calculation ----
def movie_age(year):
    """
    Calculate the age of a movie based on its release year.

    :param year: Release year of the movie.
    :type year: int
    :return: Age of the movie in years.
    :rtype: int
    """
    return date.today().year - year
