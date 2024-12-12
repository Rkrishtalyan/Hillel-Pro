from django.db import models
from elasticsearch_dsl.connections import connections
from test_app.client.models import Client

connections.create_connection(hosts=['http://localhost:9201'])

class Pet(models.Model):
    name = models.CharField(max_length=50)
    species = models.CharField(max_length=50)
    breed = models.CharField(max_length=50)
    owner = models.ForeignKey(Client, on_delete=models.CASCADE, null=True, blank=True, related_name='owners')

    def __str__(self):
        return {self.name}
