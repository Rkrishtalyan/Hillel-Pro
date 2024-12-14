from django.db import models
from django.contrib.auth.models import User
import uuid


class Task(models.Model):
    """
    Represent a task with details such as title, status, priority, and due date.

    Tasks can have a variety of states and priority levels, and can optionally
    include a description and a due date.

    :var title: The title of the task.
    :type title: str
    :var description: Additional details about the task.
    :type description: str or None
    :var status: The current status of the task.
    :type status: str
    :var priority: The priority level of the task.
    :type priority: int
    :var due_date: The due date for completing the task.
    :type due_date: datetime.date or None
    :var created_at: The date and time when the task was created.
    :type created_at: datetime.datetime
    :var updated_at: The date and time when the task was last updated.
    :type updated_at: datetime.datetime
    """

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("in progress", "In progress"),
        ("completed", "Completed"),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    priority = models.IntegerField(default=1)
    due_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        """
        Return a string representation of the task.

        :return: The title of the task.
        :rtype: str
        """
        return self.title


class Token(models.Model):
    """
    Represent an authentication token associated with a user.

    Tokens are unique and used for authenticating users in the application.

    :var key: The unique token key.
    :type key: uuid.UUID
    :var user: The user associated with the token.
    :type user: User
    """

    key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        """
        Return a string representation of the token.

        :return: A string combining the username and token key.
        :rtype: str
        """
        return f"{self.user.username} - {self.key}"
