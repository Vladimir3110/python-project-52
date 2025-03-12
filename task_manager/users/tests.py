from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.test import Client, TestCase
from django.urls import reverse


class UserCRUDTests(TestCase):
    fixtures = ['users.json']

    def setUp(self):
        self.user = User.objects.get(username='testuser')
        self.client = Client()

    def test_user_registration(self):
        """
        Тест регистрации нового пользователя (Create).
        """
        url = reverse('user_create')
        data = {
            'username': 'newuser',
            'password': 'newpassword123',
            'password_confirm': 'newpassword123',
            'first_name': 'New',
            'last_name': 'User'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())
        
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Пользователь успешно "
        "зарегистрирован")

    def test_user_update(self):
        """
        Тест обновления данных пользователя (Update).
        """
        self.client.login(username='testuser', password='testpassword123')
        url = reverse('user_update', args=[self.user.id])
        data = {
            'first_name': 'Updated',
            'last_name': 'User',
            'username': 'testuser',
            'current_password': 'testpassword123'
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 302)
        updated_user = User.objects.get(id=self.user.id)
        self.assertEqual(updated_user.first_name, 'Updated')
        
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Пользователь успешно изменен")

    def test_user_update_no_permission(self):
        """
        Тест попытки обновления чужого пользователя (Update без прав).
        """
        another_user = User.objects.create_user(
            username='anotheruser',
            password='anotherpassword123'
        )
        self.client.login(username='testuser', password='testpassword123')
        url = reverse('user_update', args=[another_user.id])
        response = self.client.post(url, {})
        # Проверяем, что доступ запрещен
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('user_list'))

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "У вас нет прав для изменения "
        "другого пользователя.")

    def test_user_delete(self):
        """
        Тест удаления пользователя (Delete).
        """
        self.client.login(username='testuser', password='testpassword123')
        url = reverse('user_delete', args=[self.user.id])
        response = self.client.post(url)
        # Проверяем, что пользователь был удален
        self.assertEqual(response.status_code, 302)
        self.assertFalse(User.objects.filter(id=self.user.id).exists())

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Пользователь успешно удален")

    def test_user_delete_no_permission(self):
        """
        Тест попытки удаления чужого пользователя (Delete без прав).
        """
        another_user = User.objects.create_user(
            username='anotheruser',
            password='anotherpassword123'
        )
        self.client.login(username='testuser', password='testpassword123')
        url = reverse('user_delete', args=[another_user.id])
        response = self.client.post(url)
        # Проверяем, что доступ запрещен
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('user_list'))

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "У вас нет прав для "
        "изменения другого пользователя.")
