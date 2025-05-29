from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from .models import Label, Task

User = get_user_model()


class TaskForm(forms.ModelForm):
    status = forms.ChoiceField(
        choices=Task.Status.choices, 
        label=_("Status"),
        widget=forms.Select(attrs={
            "id": "id_status", 
            "class": "form-select", 
            "name": "status"
            }),
        required=False,
#        initial=''
#        initial=Task.Status.NEW
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
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control', 
                'id': 'id_name', 
                'placeholder': _('Name')}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'assigned_to': forms.Select(attrs={'class': 'form-select'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['assigned_to'].queryset = User.objects.all()
        self.fields['labels'].queryset = Label.objects.all()
        self.fields['status'].choices = [('', '---------')] + list(
            Task.Status.choices)
