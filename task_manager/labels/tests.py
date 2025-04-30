from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from task_manager.labels.models import Label
from task_manager.tasks.models import Task

User = get_user_model()


class LabelTests(TestCase):
    def setUp(self):
        # Создаем тестового пользователя
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # Создаем тестовую метку
        self.label = Label.objects.create(name='bug')
        
        # Создаем тестовую задачу и связываем с меткой
        self.task = Task.objects.create(
            name='Test Task',
            description='Test Description',
            author=self.user,
            status='new'
        )
        self.task.labels.add(self.label)

    def login(self):
        self.client.force_login(self.user)

    # Тесты отображения списка меток
    def test_list_of_labels_for_authorized_user(self):
        """Проверка отображения списка меток для вошедшего пользователя"""
        self.login()
        response = self.client.get(reverse('labels_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'bug')
        self.assertTemplateUsed(response, 'labels/label_list.html')

    def test_list_of_labels_for_unauthorized_user(self):
        """Проверка редиректа для неавторизованного пользователя"""
        response = self.client.get(reverse('labels_list'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/labels/')

    # Тесты создания меток
    def test_display_label_creation_form(self):
        """Проверка доступности формы создания метки"""
        self.login()
        response = self.client.get(reverse('label_create'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _('Create label'))
        self.assertTemplateUsed(response, 'labels/label_form.html')

    def test_successful_creation_of_new_label(self):
        """Проверка успешного создания метки"""
        self.login()
        response = self.client.post(reverse('label_create'), 
                                    {'name': 'feature'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('labels_list'))
        self.assertEqual(Label.objects.count(), 2)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), _('Label created successfully'))

    # Тесты обновления меток
    def test_successful_label_update(self):
        """Проверка успешного изменения метки"""
        self.login()
        response = self.client.post(
            reverse('label_update', args=[self.label.pk]),
            {'name': 'critical bug'}
        )
        self.assertEqual(response.status_code, 302)
        self.label.refresh_from_db()
        self.assertEqual(self.label.name, 'critical bug')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), _('Label updated successfully'))

    # Тесты удаления меток
    def test_successful_removal_of_unused_label(self):
        """Проверка удаления метки без привязки к задачам"""
        new_label = Label.objects.create(name='to delete')
        self.login()
        response = self.client.post(reverse('label_delete', 
                                            args=[new_label.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Label.objects.count(), 1)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), _('Label deleted successfully'))

    def test_protection_from_deleting_used_label(self):
        """Проверка запрета удаления связанной с задачей метки"""
        self.login()
        response = self.client.post(reverse('label_delete', 
                                            args=[self.label.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Label.objects.count(), 1)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 
                         _('Cannot delete label associated with tasks'))

    # Тесты авторизации
    def test_access_to_create_tag_without_authorization(self):
        """Проверка запрета доступа к созданию метки без входа"""
        response = self.client.get(reverse('label_create'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/labels/create/')

    def test_access_to_editing_without_authorization(self):
        """Проверка запрета доступа к редактированию без входа"""
        response = self.client.get(reverse('label_update', 
                                           args=[self.label.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, 
                             f'/login/?next=/labels/{self.label.pk}/update/')

    def test_access_to_delete_without_authorization(self):
        """Проверка запрета доступа к удалению без входа"""
        response = self.client.get(reverse('label_delete', 
                                           args=[self.label.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, 
                             f'/login/?next=/labels/{self.label.pk}/delete/')
