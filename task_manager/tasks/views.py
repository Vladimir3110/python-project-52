from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from task_manager.labels.models import Label

from .forms import TaskForm
from .models import Task, User


class TaskListView(LoginRequiredMixin, View):
    def get(self, request):
        params = request.GET
        tasks = Task.objects.all().prefetch_related('labels')
        
        if status := params.get('status'):
            tasks = tasks.filter(status=status)
        if executor := params.get('executor'):
            tasks = tasks.filter(assigned_to=executor)
        if params.get('self_tasks'):
            tasks = tasks.filter(author=request.user)
        if label_id := params.get('label'):
            tasks = tasks.filter(labels__id=label_id)
        
        context = {
            'tasks': tasks,
            'statuses': Task.Status.choices,
            'executors': User.objects.all(),
            'labels': Label.objects.all(),
            'selected_status': params.get('status'),
            'selected_executor': params.get('executor'),
            'selected_label': params.get('label'),
            'self_tasks': params.get('self_tasks', False),
        }
        return render(request, 'tasks/task_list.html', context)


class TaskCreateView(LoginRequiredMixin, View):
    def get(self, request):
        form = TaskForm()
        return render(request, 'tasks/task_form.html', {'form': form})

    def post(self, request):
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.author = request.user
            task.save()
            messages.success(request, 'Задача успешно создана')
            return redirect('tasks:list')
        return render(request, 'tasks/task_form.html', {'form': form})


class TaskUpdateView(LoginRequiredMixin, View):
    def get(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        form = TaskForm(instance=task)
        return render(request, 'tasks/task_form.html', {'form': form})

    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Задача успешно изменена')
            return redirect('tasks:list')
        return render(request, 'tasks/task_form.html', {'form': form})


class TaskDeleteView(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        """Общая проверка перед любым методом"""
        self.task = get_object_or_404(Task, pk=kwargs['pk'])
        if self.task.author != request.user:
            messages.error(request, 'Задачу может удалить только ее автор')
            return redirect('tasks:list')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, pk):
        return render(request, 'tasks/task_confirm_delete.html', 
                      {'task': self.task})

    def post(self, request, pk):
        self.task.delete()
        messages.success(request, 'Задача успешно удалена')
        return redirect('tasks:list')


class TaskDetailView(LoginRequiredMixin, View):
    def get(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        return render(request, 'tasks/task_detail.html', {'task': task})
