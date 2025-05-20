from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse
from django.utils.translation import gettext as _

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task


class TaskCRUDTest(TestCase):
    fixtures = ['test_users.json', 'test_statuses.json', 
                'test_labels.json', 'test_tasks.json']

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.get(pk=1)
        cls.status = Status.objects.get(pk=1)
        cls.label = Label.objects.get(pk=1)
        cls.task = Task.objects.get(pk=1)

    def setUp(self):
        self.client.force_login(self.user)

    def test_task_creation(self):
        initial_count = Task.objects.count()
        form_data = {
            'name': 'Test task 1',
            'description': 'Sample description 1',
            'status': Task.Status.NEW,
            'labels': [self.label.id],
            'assigned_to': self.user.id,
        }
        response = self.client.post(reverse('tasks:create'), form_data)
    
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Task.objects.count(), initial_count + 1)

    def test_task_update(self):
        updated_data = {
            'name': 'Test task 2',
            'description': 'Sample description 2',
            'status': Task.Status.IN_PROGRESS,
            'labels': [self.label.id],
            'assigned_to': self.user.id
        }   
        response = self.client.post(
            reverse('tasks:update', kwargs={'pk': self.task.pk}),
            updated_data
        )
        self.assertEqual(response.status_code, 302)
        self.task.refresh_from_db()
        self.assertEqual(self.task.name, 'Test task 2')

    def test_task_delete_by_author(self):
        initial_count = Task.objects.count()
        response = self.client.post(
            reverse('tasks:delete', kwargs={'pk': self.task.pk})
        )
        self.assertEqual(Task.objects.count(), initial_count - 1)
        self.assertRedirects(response, reverse('tasks:list'))

    def test_task_delete_by_non_author(self):
        non_author = User.objects.create_user(
            username='non_author',
            password='testpassword'
        )
        self.client.force_login(non_author)
        
        initial_count = Task.objects.count()
        response = self.client.post(
            reverse('tasks:delete', kwargs={'pk': self.task.pk})
        )
        self.assertEqual(Task.objects.count(), initial_count)
        self.assertRedirects(response, reverse('tasks:list'))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), _(
            'Задачу может удалить только ее автор'))

    def test_task_detail_view(self):
        response = self.client.get(
            reverse('tasks:detail', kwargs={'pk': self.task.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.task.name)
