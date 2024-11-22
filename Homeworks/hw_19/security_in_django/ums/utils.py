# ---- Imports ----
from django.db import connection
from django.contrib.auth.models import User


def get_user_by_username_sql(username):
    """
    Retrieve a user's details from the database using raw SQL.

    Executes a parameterized SQL query to fetch the user's ID, username,
    and email from the `auth_user` table.

    :param username: The username of the user to look up.
    :type username: str
    :return: A dictionary with the user's ID, username, and email,
             or None if no user is found.
    :rtype: dict or None
    """
    with connection.cursor() as cursor:
        # Use parameterized query to prevent SQL injection
        cursor.execute(
            "SELECT id, username, email FROM auth_user WHERE username = %s",
            [username]
        )
        row = cursor.fetchone()

    if row:
        return {'id': row[0], 'username': row[1], 'email': row[2]}
    else:
        return None


def get_user_by_username_orm(username):
    """
    Retrieve a user instance using Django's ORM.

    Attempts to fetch a User object matching the provided username.
    Returns None if no user is found.

    :param username: The username of the user to look up.
    :type username: str
    :return: The User object or None if no user is found.
    :rtype: User or None
    """
    try:
        return User.objects.get(username=username)
    except User.DoesNotExist:
        return None
