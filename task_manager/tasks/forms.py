from django.contrib.auth import get_user_model
from django.forms import ModelForm

from .models import Task

User = get_user_model()


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'assigned_to', 'labels']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['assigned_to'].queryset = User.objects.all()

