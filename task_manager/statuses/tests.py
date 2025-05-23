from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from .models import Status


class StatusCRUDTests(TestCase):
    fixtures = [
        'users.json',
        'statuses.json'
    ]

    def setUp(self):
        self.client = Client()
        User = get_user_model()

        self.user = User.objects.first()
        self.client.force_login(self.user)
        self.status = Status.objects.first()

    def test_status_list_view(self):
        response = self.client.get(reverse('status_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.status.name)

#    def test_status_create_view(self):
#        self.client.login(username='testuser', password='testpass123')
#        response = self.client.post(reverse('status_create'), {
#            'name': 'New Status'})
#        self.assertEqual(response.status_code, 302)
#        self.assertTrue(Status.objects.filter(name='New Status').exists())

    def test_status_create_view(self):
        self.client.login(username='testuser', password='testpass123')
    
        response = self.client.get(reverse('status_create'))
        self.assertEqual(response.status_code, 200)
    
        response = self.client.post(
            reverse('status_create'),
            {'name': 'New Status'},
            follow=True
        )
        self.assertRedirects(response, reverse('status_list'))
        self.assertTrue(Status.objects.filter(name='New Status').exists())

    def test_status_delete_protected(self):
        self.client.login(username='testuser', password='testpass123')
        # .....

    def test_unauthenticated_access(self):
        self.client.logout()
        status = Status.objects.first()
        urls = [
            reverse('status_list'),
            reverse('status_create'),
            reverse('status_update', args=[status.id]),
            reverse('status_delete', args=[status.id])
        ]
        for url in urls:
            response = self.client.get(url)
            self.assertRedirects(response, f"/login/?next={url}")
