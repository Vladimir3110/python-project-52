from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext_lazy as _
from django.views import View

# from django.views.generic import CreateView
from django_filters.views import FilterView

from task_manager.labels.models import Label
from task_manager.statuses.models import Status

from .filters import TaskFilter
from .forms import TaskForm
from .models import Task

User = get_user_model()


class TaskListView(FilterView):
    model = Task
    filterset_class = TaskFilter
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'

#    def get_context_data(self, **kwargs):
#        context = super().get_context_data(**kwargs)
#        context.update({
#            # Исправлено имя на 'executors'
#            'executors': User.objects.all(),
#            'labels': Label.objects.all(),
#            'selected_status': self.request.GET.get('status', ''),
#            # Исправлено имя на 'executor' (было 'assigned_to')
#            'selected_executor': self.request.GET.get('executor', ''),
#            'selected_label': self.request.GET.get('label', ''),
#            'self_tasks': self.request.GET.get('self_tasks', '') == 'on'
#        })
#        return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'executors': User.objects.all(),
            'labels': Label.objects.all(),
            'selected_status': self.request.GET.get('status', ''),
            'selected_assigned_to': self.request.GET.get('assigned_to', ''),
            'selected_label': self.request.GET.get('label', ''),
            'self_tasks': self.request.GET.get('self_tasks', '') == 'on'
        })
        return context
    
    def get_filterset_kwargs(self, filterset_class):
        kwargs = super().get_filterset_kwargs(filterset_class)
        kwargs['request'] = self.request
        kwargs['data'] = self.request.GET
        return kwargs


# class TaskCreateView(CreateView):
#    model = Task
#    form = TaskForm
#    template_name = ('tasks/task_form.html', {'form': form})

class TaskCreateView(LoginRequiredMixin, View):
    def get(self, request):
        form = TaskForm()
        if not Status.objects.exists():
            Status.objects.create(name="Default Status")
#        print("Available statuses:", Status.objects.all())
        return render(request, 'tasks/task_form.html', {'form': form})

    def post(self, request):
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.author = request.user
            task.save()
            form.save_m2m()
            messages.success(request, _('Task created successfully!'))
            return redirect('tasks:list')
#        print("Form errors:", form.errors)
#        print("Form data:", request.POST)  # Вывод данных
#        print("Form errors:", form.errors)
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
            messages.success(request, _('Task updated successfully'))
            return redirect('tasks:list')
        return render(request, 'tasks/task_form.html', {'form': form})


class TaskDeleteView(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        """Общая проверка перед любым методом"""
        self.task = get_object_or_404(Task, pk=kwargs['pk'])
        if self.task.author != request.user:
            messages.error(request, _('Only task author can delete it'))
            return redirect('tasks:list')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, pk):
        return render(request, 'tasks/task_confirm_delete.html', 
                      {'task': self.task})

    def post(self, request, pk):
        self.task.delete()
        messages.success(request, _('Task deleted successfully'))
        return redirect('tasks:list')


class TaskDetailView(LoginRequiredMixin, View):
    def get(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        return render(request, 'tasks/task_detail.html', {'task': task})
