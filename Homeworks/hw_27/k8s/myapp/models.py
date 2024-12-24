from django.db import models


class Entry(models.Model):
    """
    Represent an entry with a title and creation timestamp.

    The Entry model provides a simple structure for storing entries
    with a title and a timestamp of when it was created.

    :var title: The title of the entry.
    :type title: str
    :var created_at: The timestamp when the entry was created.
    :type created_at: datetime
    """

    title = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Return the string representation of the entry.

        :return: The title of the entry.
        :rtype: str
        """
        return self.title
