from django.db import models
from elasticsearch_dsl import Document, Text, Date
from elasticsearch_dsl.connections import connections

connections.create_connection(hosts=['http://localhost:9202'])


class DataDocument(models.Model):
    """
    Represent a data document with title, description, and creation date.

    This model is used to store metadata about a document in a database.

    :var title: The title of the document.
    :type title: str
    :var description: A detailed description of the document.
    :type description: str
    :var created_at: The timestamp when the document was created.
    :type created_at: datetime
    """

    title = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    # Uncomment the following block if you need an Elasticsearch index
    # class Index:
    #     """
    #     Define Elasticsearch index settings for the model.
    #
    #     :var name: Name of the Elasticsearch index.
    #     :type name: str
    #     """
    #     name = 'data_index'
    #
    # def save(self, **kwargs):
    #     """
    #     Override the save method to include additional behavior.
    #
    #     :param kwargs: Additional keyword arguments for saving.
    #     :return: Result of the super save method.
    #     """
    #     return super().save(**kwargs)

    def __str__(self):
        """
        Return the string representation of the DataDocument instance.

        :return: Title of the document.
        :rtype: str
        """
        return self.title
