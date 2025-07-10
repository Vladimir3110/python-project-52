from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from task_manager.labels.models import Label
from task_manager.statuses.models import Status

User = get_user_model()


class Task(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Name'))
    description = models.TextField(verbose_name=_('Description'))

    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        related_name='tasks',
        verbose_name=_('Status')
    )

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
    labels = models.ManyToManyField(
        Label,
        blank=True,
        related_name='tasks',
        verbose_name=_('Labels')
    )

    created_at = models.DateTimeField(auto_now_add=True)

#    created_at = models.DateTimeField(auto_now_add=True, 
#                                      verbose_name=_('Created at'))

    def __str__(self):
        return self.name
