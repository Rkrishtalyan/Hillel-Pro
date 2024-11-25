from datetime import timedelta
from django.utils import timezone
import pytest

from .serializers import TaskWithUserSerializer


# ---- Fixtures for Test Data ----
@pytest.fixture
def future_date():
    """
    Provide a future date fixture for testing.

    :return: A date object representing tomorrow.
    :rtype: date
    """
    return timezone.now().date() + timedelta(days=1)


@pytest.fixture
def valid_user_data():
    """
    Provide a fixture for valid user data.

    :return: A dictionary with valid user data.
    :rtype: dict
    """
    return {
        'username': 'testuser',
        'email': 'testuser@example.com'
    }


@pytest.fixture
def invalid_user_data():
    """
    Provide a fixture for invalid user data missing required fields.

    :return: A dictionary with invalid user data.
    :rtype: dict
    """
    return {
        'email': 'testuser@example.com'
    }


@pytest.fixture
def valid_task_data_with_user(future_date, valid_user_data):
    """
    Provide a fixture for valid task data including a valid user.

    :param future_date: A fixture providing a future due date.
    :type future_date: date
    :param valid_user_data: A fixture providing valid user data.
    :type valid_user_data: dict
    :return: A dictionary with valid task data.
    :rtype: dict
    """
    return {
        'title': 'Collaborate on Project',
        'description': 'Work with the team',
        'due_date': future_date,
        'user': valid_user_data
    }


@pytest.fixture
def invalid_task_data_with_invalid_user(future_date, invalid_user_data):
    """
    Provide a fixture for task data with invalid nested user data.

    :param future_date: A fixture providing a future due date.
    :type future_date: date
    :param invalid_user_data: A fixture providing invalid user data.
    :type invalid_user_data: dict
    :return: A dictionary with invalid task data.
    :rtype: dict
    """
    return {
        'title': 'Task with Invalid User',
        'description': 'User data is invalid',
        'due_date': future_date,
        'user': invalid_user_data
    }


# ---- Test Cases for TaskSerializer2 with Nested User ----
@pytest.mark.parametrize(
    "task_data_fixture, expected_validity, error_field",
    [
        # Valid nested data
        ('valid_task_data_with_user', True, None),
        # Invalid nested user data
        ('invalid_task_data_with_invalid_user', False, 'user'),
    ]
)
def test_task_serializer_with_nested_user(request, task_data_fixture, expected_validity, error_field):
    """
    Test TaskSerializer2 with nested user data.

    :param request: The pytest request object to access fixtures dynamically.
    :type request: _pytest.fixtures.FixtureRequest
    :param task_data_fixture: The name of the fixture to retrieve task data.
    :type task_data_fixture: str
    :param expected_validity: Whether the serializer should be valid.
    :type expected_validity: bool
    :param error_field: The expected error field if validation fails.
    :type error_field: str or None
    :raises AssertionError: If the serializer's validity does not match expectations.
    """
    task_data = request.getfixturevalue(task_data_fixture)
    serializer = TaskWithUserSerializer(data=task_data)
    is_valid = serializer.is_valid()
    assert is_valid == expected_validity
    if not is_valid and error_field:
        assert error_field in serializer.errors
        if error_field == 'user':
            assert 'username' in serializer.errors['user']
