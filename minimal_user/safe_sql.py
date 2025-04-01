from typing import Tuple, Optional
from django.db import connection


def find_user_by_username(username: str) -> Optional[Tuple[int, str, str]]:
    """
    Safely looks up a user in the database by their username using a parameterized query.
    :param username: The username to search for.
    :return: A tuple containing (id, username, email) if found,
        or None if no user matches the given username.
    """
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT id, username, email FROM auth_user WHERE username = %s",
            (username,))
        return cursor.fetchone()
