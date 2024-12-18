from django.db import models


class Test(models.Model):
    """
    Represent a test entry with a title and creation timestamp.

    The Test model is a simple representation of a database entry with a
    title and automatic timestamp.

    :var title: The title of the entry.
    :type title: str
    :var created_at: The timestamp of when the entry was created.
    :type created_at: datetime
    """

    title = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Return the string representation of the Test instance.

        :return: The title of the entry.
        :rtype: str
        """
        return self.title
