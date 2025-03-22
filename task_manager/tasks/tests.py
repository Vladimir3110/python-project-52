from django.contrib.auth import get_user_model

# from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

from .models import Task

User = get_user_model()


class TaskCRUDTest(TestCase):
    def setUp(self):
        self.main_user = User.objects.create_user(
            username='testuser',
            password='testpass'
        )

        self.other_user = User.objects.create_user(
            username='otheruser',
            password='testpass'
        )
        
        self.task = Task.objects.create(
            name="Test Task",
            description="Test Description",
            status="in_progress",
            author=self.main_user
        )

        self.client.force_login(self.main_user)

    def test_task_creation(self):
        response = self.client.post(reverse('tasks:create'), {
            'name': 'New Task',
            'description': 'New Description',
            'status': 'in_progress'
        })
        self.assertEqual(Task.objects.count(), 2)
        self.assertRedirects(response, reverse('tasks:list'))

    def test_task_delete_by_author(self):
        response = self.client.post(reverse('tasks:delete', 
                                            args=[self.task.id]))
        self.assertEqual(Task.objects.count(), 0)
        self.assertRedirects(response, reverse('tasks:list'))

    def test_task_delete_by_non_author(self):
        self.client.force_login(self.other_user)
    
        response = self.client.post(
            reverse('tasks:delete', args=[self.task.id]),
            follow=True
        )
    
        self.assertEqual(Task.objects.count(), 1)
        messages = list(response.context['messages'])
        self.assertTrue(len(messages) > 0, "Сообщение не найдено")
        self.assertIn("Задачу может удалить только ее автор", str(messages[0]))
