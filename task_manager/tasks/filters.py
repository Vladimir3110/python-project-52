import django_filters
from django import forms
from django.contrib.auth.models import User

from task_manager.labels.models import Label
from task_manager.tasks.models import Task


class TaskFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(
        choices=Task.Status.choices,
        label='Статус',
        field_name='status'
    )
    executor = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        label='Исполнитель',
        field_name='assigned_to'
    )
    label = django_filters.ModelChoiceFilter(
        queryset=Label.objects.all(),
        label='Метка',
        field_name='labels'
    )
    self_tasks = django_filters.BooleanFilter(
        method='filter_self_tasks',
        label='Только свои задачи',
        widget=forms.CheckboxInput(),
        field_name='self_tasks'
    )

    class Meta:
        model = Task
        fields = ['status', 'executor', 'label', 'self_tasks']

    def filter_self_tasks(self, queryset, name, value):
        value = value == 'on' if isinstance(value, str) else value
        
        if value and self.request and self.request.user.is_authenticated:
            return queryset.filter(author=self.request.user)
        return queryset
