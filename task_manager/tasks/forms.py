from django import forms
from django.forms import ModelForm

from .models import Task


class TaskForm(ModelForm):
    executor = forms.ModelChoiceField(
        queryset=Task._meta.get_field('assigned_to').
        remote_field.model.objects.all(),
        label=Task._meta.get_field('assigned_to').verbose_name,
        required=False
    )

    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor', 'labels']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance.pk:
            self.initial['executor'] = self.instance.assigned_to
            
    def save(self, commit=True):
        task = super().save(commit=False)
        task.assigned_to = self.cleaned_data['executor']
        if commit:
            task.save()
            self.save_m2m()
        return task
