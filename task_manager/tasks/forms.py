from django import forms
from django.utils.translation import gettext_lazy as _

from task_manager.labels.models import Label

from .models import Task


class TaskForm(forms.ModelForm):
    status = forms.ChoiceField(
        choices=Task.Status.choices,
        label=_("Status"),
        required=True
    )
    labels = forms.ModelMultipleChoiceField(
        queryset=Label.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-select'}),
        required=False,
        label=_("Labels")
    )
    
    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'assigned_to', 'labels']
        labels = {
            'name': _("Name"),
            'description': _("Description"),
            'status': _("Status"),
            'assigned_to': _("Assignee"),
            'labels': _("Labels")
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
#        self.fields['status'].queryset = Status.objects.all()
        self.fields['labels'].queryset = Label.objects.all()
