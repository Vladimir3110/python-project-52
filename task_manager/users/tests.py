from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

from task_manager.statuses.models import Status
from task_manager.tasks.models import Task

User = get_user_model()


class UserCRUDTests(TestCase):
    fixtures = ['users.json', 'statuses.json']

    def setUp(self):
        self.user1 = User.objects.get(pk=1)
        self.user2 = User.objects.get(pk=2)
        self.user3 = User.objects.get(pk=3)
        self.users_count = User.objects.count()
        self.client.login(username='testuser', password='testpass123')
        self.status = Status.objects.get(pk=1)

    def test_user_registration(self):
        initial_users = User.objects.count()

        url = reverse('user_create')
        data = {
            'username': 'newuser',
            'password1': 'newpassword123',
            'password2': 'newpassword123',
            'first_name': 'New',
            'last_name': 'User'
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(User.objects.count(), initial_users + 1)
        self.assertTrue(User.objects.filter(username='newuser').exists())

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 
                         "Пользователь успешно зарегистрирован")

    def test_user_update(self):
        self.client.login(username='user1', password='testpass123')
        url = reverse('user_update', kwargs={'pk': self.user1.pk})
        response = self.client.post(
            url,
            {
                'username': 'testuser',
                'first_name': 'Updated',
                'last_name': 'User',
                'password1': 'testpass123',
                'password2': 'testpass123',
            },
        )
        self.assertRedirects(response, reverse('user_list'))
        self.user1.refresh_from_db()
        self.assertEqual(self.user1.first_name, 'Updated')
        self.assertEqual(self.user1.last_name, 'User')
#        print("\nТест: Данные пользователя успешно обновлены")

    def test_unauthenticated_user_cannot_update(self):
        self.client.logout()
        url = reverse('user_update', kwargs={'pk': self.user1.pk})
        response = self.client.post(url)
    
        login_url = reverse(settings.LOGIN_URL)
        expected_redirect = f"{login_url}?next={url}"
        self.assertRedirects(response, expected_redirect)
    
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 
                        "Вы не авторизованы! Пожалуйста, выполните вход.")


class UserDeleteViewTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', 
                                              password='testpass123')
        self.user2 = User.objects.create_user(username='user2', 
                                              password='testpass123')
        self.status = Status.objects.create(name='Test Status')

    def test_unauthenticated_user_cannot_delete(self):
        url = reverse('user_delete', kwargs={'pk': self.user1.pk})
        response = self.client.post(url)
        login_url = reverse(settings.LOGIN_URL)
        expected_redirect = f"{login_url}?next={url}"
    
        self.assertRedirects(response, expected_redirect)
        self.assertTrue(User.objects.filter(pk=self.user1.pk).exists())
    
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Вы не авторизованы! "
        "Пожалуйста, выполните вход.")

    def test_user_cannot_delete_other_user(self):
        self.client.login(username='user1', password='testpass123')
        url = reverse('user_delete', kwargs={'pk': self.user2.pk})
        response = self.client.post(url)
        self.assertRedirects(response, reverse('user_list'))
        self.assertTrue(User.objects.filter(pk=self.user2.pk).exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "У вас нет прав для изменения "
        "другого пользователя.")

    def test_cannot_delete_user_with_tasks(self):
        Task.objects.create(
            name='Test task 1', 
            author=self.user1,
            status=self.status
        )

        self.client.login(username='user1', password='testpass123')
        url = reverse('user_delete', kwargs={'pk': self.user1.pk})
        response = self.client.post(url)
        self.assertRedirects(response, reverse('user_list'))
        self.assertTrue(User.objects.filter(pk=self.user1.pk).exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertIn("Невозможно удалить пользователя, потому "
        "что он используется", str(messages[0]))

    def test_successful_user_deletion(self):
        self.client.login(username='user1', password='testpass123')
        url = reverse('user_delete', kwargs={'pk': self.user1.pk})
        response = self.client.post(url)
        self.assertRedirects(response, reverse('user_list'))
        self.assertFalse(User.objects.filter(pk=self.user1.pk).exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Пользователь успешно удален")
