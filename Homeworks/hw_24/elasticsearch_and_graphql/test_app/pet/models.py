from django.db import models
from elasticsearch_dsl.connections import connections
from test_app.client.models import Client

connections.create_connection(hosts=['http://localhost:9201'])


class Pet(models.Model):
    """
    Represent a pet with its details and owner information.

    The Pet model includes attributes for the pet's name, species, breed,
    and a reference to its owner.

    :var name: The name of the pet.
    :type name: str
    :var species: The species of the pet (e.g., dog, cat).
    :type species: str
    :var breed: The breed of the pet.
    :type breed: str
    :var owner: A foreign key referencing the pet's owner (Client).
    :type owner: Client
    """

    name = models.CharField(max_length=50)
    species = models.CharField(max_length=50)
    breed = models.CharField(max_length=50)
    owner = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='owners'
    )

    def __str__(self):
        """
        Return the string representation of the Pet instance.

        :return: Name of the pet.
        :rtype: str
        """
        return self.name
