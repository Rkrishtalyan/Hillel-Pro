from datetime import timedelta
from django.utils import timezone
import pytest

from .serializers import TaskSerializer


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
def past_date():
    """
    Provide a past date fixture for testing.

    :return: A date object representing yesterday.
    :rtype: date
    """
    return timezone.now().date() - timedelta(days=1)


@pytest.fixture
def valid_task_data(future_date):
    """
    Provide a fixture for valid task data.

    :param future_date: A fixture providing a future due date.
    :type future_date: date
    :return: A dictionary with valid task data.
    :rtype: dict
    """
    return {
        'title': 'Prepare Presentation',
        'description': 'Slides for the meeting',
        'due_date': future_date
    }


@pytest.fixture
def invalid_task_data_missing_title(future_date):
    """
    Provide a fixture for invalid task data missing the title.

    :param future_date: A fixture providing a future due date.
    :type future_date: date
    :return: A dictionary with missing title.
    :rtype: dict
    """
    return {
        'description': 'Missing title field',
        'due_date': future_date
    }


@pytest.fixture
def invalid_task_data_due_date_in_past(past_date):
    """
    Provide a fixture for invalid task data with a past due date.

    :param past_date: A fixture providing a past due date.
    :type past_date: date
    :return: A dictionary with a past due date.
    :rtype: dict
    """
    return {
        'title': 'Past Task',
        'description': 'Due date is in the past',
        'due_date': past_date
    }


# ---- Test Cases for TaskSerializer ----
def test_task_serializer_valid_data(valid_task_data):
    """
    Test that the TaskSerializer is valid with correct data.

    :param valid_task_data: A fixture providing valid task data.
    :type valid_task_data: dict
    :raises AssertionError: If the serializer is not valid.
    """
    serializer = TaskSerializer(data=valid_task_data)
    assert serializer.is_valid()


def test_task_serializer_missing_title(invalid_task_data_missing_title):
    """
    Test that the TaskSerializer is invalid when the title is missing.

    :param invalid_task_data_missing_title: A fixture with missing title.
    :type invalid_task_data_missing_title: dict
    :raises AssertionError: If the serializer is valid with missing title.
    """
    serializer = TaskSerializer(data=invalid_task_data_missing_title)
    assert not serializer.is_valid()
    assert 'title' in serializer.errors


def test_task_serializer_due_date_in_past(invalid_task_data_due_date_in_past):
    """
    Test that the TaskSerializer is invalid with a past due date.

    :param invalid_task_data_due_date_in_past: A fixture with a past due date.
    :type invalid_task_data_due_date_in_past: dict
    :raises AssertionError: If the serializer is valid with a past due date.
    """
    serializer = TaskSerializer(data=invalid_task_data_due_date_in_past)
    assert not serializer.is_valid()
    assert 'due_date' in serializer.errors
