from datetime import timedelta
from django.test import TestCase
from django.utils import timezone
import pytest

from .forms import TaskForm


# ---- OOP Approach Using Unittest ----
class TaskFormTestCase(TestCase):
    """
    Test case for the TaskForm using the unittest framework.

    This class contains tests for validating form input data,
    ensuring required fields are checked, and handling invalid due dates.
    """

    def test_form_valid_data(self):
        """
        Test that the form is valid when provided with correct data.

        :raises AssertionError: If the form is not valid when expected to be.
        """
        future_date = timezone.now().date() + timedelta(days=1)
        form_data = {
            'title': 'Complete Homework',
            'description': 'Math exercises',
            'due_date': future_date
        }
        form = TaskForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_missing_required_fields(self):
        """
        Test that the form is invalid when required fields are missing.

        :raises AssertionError: If the form is valid when missing required fields.
        """
        form_data = {
            'description': 'No title provided',
            'due_date': '2024-01-01'
        }
        form = TaskForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)

    def test_form_due_date_in_past(self):
        """
        Test that the form is invalid when the due date is in the past.

        :raises AssertionError: If the form is valid with a past due date.
        """
        past_date = timezone.now().date() - timedelta(days=1)
        form_data = {
            'title': 'Past Task',
            'description': 'This task has a past due date',
            'due_date': past_date
        }
        form = TaskForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('due_date', form.errors)


# ---- Functional Approach Using Pytest ----
def test_task_form_valid_data():
    """
    Test that the form is valid when provided with correct data using pytest.

    :raises AssertionError: If the form is not valid when expected to be.
    """
    future_date = timezone.now().date() + timedelta(days=1)
    form_data = {
        'title': 'Buy Groceries',
        'description': 'Milk and eggs',
        'due_date': future_date
    }
    form = TaskForm(data=form_data)
    assert form.is_valid()


def test_task_form_missing_required_fields():
    """
    Test that the form is invalid when required fields are missing using pytest.

    :raises AssertionError: If the form is valid when missing required fields.
    """
    form_data = {
        'description': 'No title provided',
        'due_date': '2024-01-01'
    }
    form = TaskForm(data=form_data)
    assert not form.is_valid()
    assert 'title' in form.errors


def test_task_form_due_date_in_past():
    """
    Test that the form is invalid when the due date is in the past using pytest.

    :raises AssertionError: If the form is valid with a past due date.
    """
    past_date = timezone.now().date() - timedelta(days=1)
    form_data = {
        'title': 'Past Due Date Task',
        'description': 'Due date is in the past',
        'due_date': past_date
    }
    form = TaskForm(data=form_data)
    assert not form.is_valid()
    assert 'due_date' in form.errors
