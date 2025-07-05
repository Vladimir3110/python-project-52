from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from task_manager.statuses.models import Status

from .models import Label, Task

User = get_user_model()


class TaskForm(forms.ModelForm):
    status = forms.ModelChoiceField(
        queryset=Status.objects.all(),
        label=_("Status"),
        widget=forms.Select(attrs={
            "id": "id_status",
            "class": "form-select",
            "name": "status"
        }),
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
            'assigned_to': _("Assignee"),
        }
        widgets = {
            'assigned_to': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['assigned_to'].queryset = User.objects.all()
        self.fields['assigned_to'].label = _("Assigned to")

        self.fields['status'].label = _("Status")

# class TaskForm(forms.ModelForm):
#    status = forms.ChoiceField(
#        choices=Task.Status.choices, 
#        label=_("Status"),
#        widget=forms.Select(attrs={
#            "id": "id_status", 
#            "class": "form-select", 
#            "name": "status"
#            }),
#        required=False,
#    )
#    labels = forms.ModelMultipleChoiceField(
#        queryset=Label.objects.all(),
#        widget=forms.SelectMultiple(attrs={'class': 'form-select'}),
#        required=False,
#        label=_("Labels")
#    )

#    class Meta:    
#        model = Task
#        fields = ['name', 'description', 'status', 'assigned_to', 'labels']

#        status = forms.ModelChoiceField(
#        queryset=Status.objects.all(),
#        label=_("Status"),
#        empty_label=None
#    )
#        labels = {
#            'name': _("Name"),
#            'description': _("Description"),
#            'status': _("Status"),
#            'assigned_to': _("Assignee"),
#            'labels': _("Labels")
#        }

#        widgets = {
#            'executor': forms.Select(
#                attrs={
#                    'class': 'form-select',
#                }
#            ),
#            'labels': forms.SelectMultiple(
#                attrs={
#                    'class': 'form-select',
#                }
#            ),
#        }
    
#    def __init__(self, *args, **kwargs):
#        super().__init__(*args, **kwargs)
#        self.fields['assigned_to'].queryset = User.objects.all()
#        self.fields['labels'].queryset = Label.objects.all()
#        self.fields['status'].choices = Task.Status.choices
#        self.fields['status'].label = _("Status")
#        self.fields['status'].choices = [('', '---------')] + list(
#            Task.Status.choices)
