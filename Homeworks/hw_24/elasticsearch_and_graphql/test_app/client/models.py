# ---- Imports ----
from django.db import models
from elasticsearch_dsl.connections import connections

# ---- Elasticsearch Connection ----
connections.create_connection(hosts=['http://localhost:9201'])


class Client(models.Model):
    """
    Represent a client with personal information and account status.

    The Client model includes attributes for storing a client's name, email,
    activity status, and registration date.

    :var first_name: The first name of the client.
    :type first_name: str
    :var last_name: The last name of the client.
    :type last_name: str
    :var email: The email address of the client.
    :type email: str
    :var is_active: Indicates whether the client is active.
    :type is_active: bool
    :var registered_at: The date and time when the client registered.
    :type registered_at: datetime
    """

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(blank=True)
    is_active = models.BooleanField(default=True)
    registered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Return the string representation of the Client instance.

        :return: Full name of the client.
        :rtype: str
        """
        return f"{self.first_name} {self.last_name}"
