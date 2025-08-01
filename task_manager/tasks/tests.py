from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse
from django.utils.translation import gettext as _

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task

User = get_user_model()


class TaskCRUDTest(TestCase):
    fixtures = ['users.json', 'statuses.json', 'labels.json', 'tasks.json']

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.get(pk=1)
        cls.status = Status.objects.get(pk=1)
        # Добавим второй статус для теста обновления
        cls.status_in_progress = Status.objects.create(name='in progress')
        cls.label = Label.objects.get(pk=1)
        cls.task = Task.objects.get(pk=1)

    def setUp(self):
        self.client.force_login(self.user)

    def test_task_creation(self):
        initial_count = Task.objects.count()
        form_data = {
            'name': 'Test task 1',
            'description': 'Sample description 1',
            'status': self.status.id,
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
            'status': self.status_in_progress.id,  # передаем ID статуса
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
