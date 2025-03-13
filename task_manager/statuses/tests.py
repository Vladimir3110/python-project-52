# from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from .models import Status


class StatusCRUDTests(TestCase):
    fixtures = ['test_data.json']

    def setUp(self):
        self.client = Client()

    def test_status_list_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('status_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Status")

    def test_status_create_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('status_create'), {
            'name': 'New Status'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Status.objects.filter(name='New Status').exists())

    def test_status_delete_protected(self):
        self.client.login(username='testuser', password='testpass123')
        # .....

    def test_unauthenticated_access(self):
        urls = [
            reverse('status_list'),
            reverse('status_create'),
            reverse('status_update', args=[1]),
            reverse('status_delete', args=[1])
        ]
        for url in urls:
            response = self.client.get(url)
            self.assertRedirects(response, f"/login/?next={url}")
