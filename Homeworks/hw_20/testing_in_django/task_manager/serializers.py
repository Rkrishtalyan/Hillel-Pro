from rest_framework import serializers
from django.utils import timezone


# ---- TaskSerializer Definition ----
class TaskSerializer(serializers.Serializer):
    """
    Represent a serializer for task data.

    This serializer handles task fields such as ID, title, description, and due date,
    and ensures that the due date is not in the past.

    :var id: The ID of the task (read-only).
    :type id: serializers.IntegerField
    :var title: The title of the task.
    :type title: serializers.CharField
    :var description: The description of the task.
    :type description: serializers.CharField
    :var due_date: The due date of the task.
    :type due_date: serializers.DateField
    """

    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=100, required=True)
    description = serializers.CharField(required=False)
    due_date = serializers.DateField(required=False)

    def validate_due_date(self, value):
        """
        Validate the due date to ensure it is not in the past.

        :param value: The due date to validate.
        :type value: date
        :return: The validated due date.
        :rtype: date
        :raises serializers.ValidationError: If the due date is in the past.
        """
        if value and value < timezone.now().date():
            raise serializers.ValidationError("Due date cannot be in the past.")
        return value


# ---- UserSerializer Definition ----
class UserSerializer(serializers.Serializer):
    """
    Represent a serializer for user data.

    This serializer handles user-related fields such as ID, username, and email.

    :var id: The ID of the user (read-only).
    :type id: serializers.IntegerField
    :var username: The username of the user.
    :type username: serializers.CharField
    :var email: The email address of the user.
    :type email: serializers.EmailField
    """

    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(max_length=100, required=True)
    email = serializers.EmailField(required=True)


# ---- TaskWithUserSerializer Definition with Nested User ----
class TaskWithUserSerializer(serializers.Serializer):
    """
    Represent a serializer for task data with a nested user.

    This serializer extends task serialization by including nested user details
    in addition to validating that the due date is not in the past.

    :var id: The ID of the task (read-only).
    :type id: serializers.IntegerField
    :var title: The title of the task.
    :type title: serializers.CharField
    :var description: The description of the task.
    :type description: serializers.CharField
    :var due_date: The due date of the task.
    :type due_date: serializers.DateField
    :var user: The nested user details.
    :type user: UserSerializer
    """

    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=100, required=True)
    description = serializers.CharField(required=False)
    due_date = serializers.DateField(required=False)
    user = UserSerializer()

    def validate_due_date(self, value):
        """
        Validate the due date to ensure it is not in the past.

        :param value: The due date to validate.
        :type value: date
        :return: The validated due date.
        :rtype: date
        :raises serializers.ValidationError: If the due date is in the past.
        """
        if value and value < timezone.now().date():
            raise serializers.ValidationError("Due date cannot be in the past.")
        return value
