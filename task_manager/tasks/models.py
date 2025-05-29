from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from task_manager.labels.models import Label

User = get_user_model()


class Task(models.Model):
    class Status(models.TextChoices):
        NEW = 'new', _('New')
        IN_PROGRESS = 'In Progress', _('In Progress')
        DONE = 'Done', _('Done')

    name = models.CharField(max_length=100, verbose_name=_('Name'))
    description = models.TextField(verbose_name=_('Description'))
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='authored_tasks',
        verbose_name=_('Author')
    )
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_tasks',
        verbose_name=_('Assigned to')
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.NEW,
        verbose_name=_('Status')
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_(
        'Created at'))

    labels = models.ManyToManyField(Label, related_name='tasks', blank=True)

    def __str__(self):
        return self.name
