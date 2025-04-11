from django import forms

from task_manager.labels.models import Label

from .models import Task

# from task_manager.statuses.models import Status


class TaskForm(forms.ModelForm):
    status = forms.ChoiceField(
        choices=Task.Status.choices,
        label="Статус",
        required=True
    )
    labels = forms.ModelMultipleChoiceField(
        queryset=Label.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-select'}),
        required=False,
        label='Метки'
    )
    
    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'assigned_to', 'labels']
        labels = {
            'name': 'Имя',
            'description': 'Описание',
            'status': 'Статус',
            'assigned_to': 'Исполнитель',
            'labels': 'Метки'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
#        self.fields['status'].queryset = Status.objects.all()
        self.fields['labels'].queryset = Label.objects.all()
