from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch
import pytest
import logging
from selenium import webdriver

from .models import Task
from .signals import task_create_signal
from .views import send_task_notification


class TaskModelTest(TestCase):
    def setUp(self):
        self.task = Task.objects.create(title='Test Task')

    def test_task_creation(self):
        self.assertEqual(self.task.title, 'Test Task')
        self.assertFalse(self.task.completed)

    def test_task_string_representation(self):
        self.assertEqual(str(self.task), 'Test Task')


class TaskViewTest(TestCase):
    def setUp(self):
        self.task = Task.objects.create(title='View Task')

    def test_task_list_view(self):
        response = self.client.get(reverse('task_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'View Task')


# ---- pytest ----

@pytest.mark.django_db
def test_task_creation():
    task = Task.objects.create(title='Test Task', completed=False)
    assert task.title == 'Test Task'
    assert not task.completed


def test_task_string_representation():
    task = Task(title='Test Task')
    assert str(task) == 'Test Task'


@pytest.mark.django_db
def test_task_list_view(client):
    Task.objects.create(title='View Task', completed=False)
    response = client.get(reverse('task_list'))
    assert response.status_code == 200
    assert "View Task" in response.content.decode()


@pytest.mark.django_db
def test_create_task(client):
    url = reverse('task_list')
    response = client.post(url, {'title': 'Test Task', 'completed': False})
    assert response.status_code == 201
    assert response.json()['title'] == 'Test Task'


# @pytest.mark.parametrize('title', 'completed', [
#     ('Task 1', False),
#     ('Task 2', True),
#     ('Task 3', False),
# ])
# @pytest.mark.django_db
# def test_task_creation_parametrized(title, completed):
#     task = Task.objects.create(title=title, completed=completed)
#     assert task.title == title
#     assert task.completed == completed


# ---- Fixture ----
@pytest.fixture
def task():
    return Task.objects.create(title='Fixture Task', completed=False)


@pytest.mark.django_db
def test_fixture_task(task):
    assert task.title == 'Fixture Task'
    assert not task.completed


# ---- UnitTest ----

@patch('tasks.views.send_mail_notification')
def test_send_task_notification(mock_send_email):
    send_task_notification('Test Task')
    mock_send_email.assert_called_once_with(
        'new_task_created',
        'task "Test Task" created',
        'example@gmail.com',
        ['email1@gmail.com', 'email2@gmail.com', 'email3@gmail.com'],
    )


@pytest.mark.django_db
def test_task_list_authentication(client):
    url = reverse('task_list')
    response = client.get(url)
    assert response.status_code == 302


def test_task_signal(mocker):
    mock_signal =mocker.patch('task.signals.task_created_signal')
    Task.objects.create(title='Signal Task')
    mock_signal.assert_called_once()


@pytest.mark.django_db
def test_export_tasks_csv(client):
    Task.objects.create(title='Export Task 1', completed=False)
    Task.objects.create(title='Export Task 2', completed=True)
    url = reverse('export_tasks_csv')
    response = client.get(url)
    assert response.status_code == 200
    assert response['Content-Type'] == 'text/csv'
    assert 'Export Task 1' in response.content.decode()
    assert 'Export Task 2' in response.content.decode()


def test_logging(mocker, client):
    mock_logger = mocker.patch('tasks.views.logger')
    client.get(reverse('task_list'))
    mock_logger.info.assert_called_once_with('task list viewed')


def test_task_creation_with_selenium():
    driver = webdriver.Chrome()
    driver.get('http://localhost:8000/tasks')
    assert 'Tasks' in driver.title
    driver.quit()
