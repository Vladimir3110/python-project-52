from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.test import Client, TestCase
from django.urls import reverse

from task_manager.tasks.models import Task

User = get_user_model()


class UserCRUDTests(TestCase):
    fixtures = ['users.json']

    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.get(pk=1)
        self.user2 = get_user_model().objects.get(pk=2)
        self.user3 = get_user_model().objects.get(pk=3)
        self.users_count = get_user_model().objects.count()

    def test_user_registration(self):
        initial_users = User.objects.all()
        self.assertEqual(initial_users.count(), 3)

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
        self.assertEqual(User.objects.count(), 4)
        self.assertTrue(User.objects.filter(username='newuser').exists())

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 
                         "Пользователь успешно зарегистрирован")

    def test_user_update(self):
        self.assertEqual(self.user.first_name, 'Test')

        login_success = self.client.login(
            username='testuser', 
            password='testpass123'
        )
        self.assertTrue(login_success)

        response = self.client.post(
            reverse('user_update', args=[self.user.id]),
            {
                'username': 'testuser',
                'first_name': 'Updated',
                'last_name': 'User',
                'password1': 'testpass123',
                'password2': 'testpass123',
            },
            follow=True
        )

        self.assertRedirects(response, reverse('user_list'))

        self.user.refresh_from_db()
    
        self.assertEqual(self.user.first_name, 'Updated')
        self.assertEqual(self.user.last_name, 'User')
#        print("\nТест: Данные пользователя успешно обновлены")

    def test_unauthenticated_user_cannot_update(self):
        url = reverse('user_update', kwargs={'pk': self.user.pk})
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
        Task.objects.create(name='Test Task', author=self.user1)
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
