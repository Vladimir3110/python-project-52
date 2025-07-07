from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from .filters import TaskFilter
from .forms import TaskForm
from .models import Task

User = get_user_model()


class TaskListView(ListView):
    model = Task
    filterset_class = TaskFilter
    context_object_name = 'tasks'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = self.filterset_class(
            self.request.GET,
            queryset=queryset,
            request=self.request
        )
        return self.filterset.qs.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filterset
        return context

# class TaskListView(FilterView):
#    model = Task
#    filterset_class = TaskFilter
#    template_name = 'tasks/task_list.html'
#    context_object_name = 'tasks'

#    def get_context_data(self, **kwargs):
#        context = super().get_context_data(**kwargs)
#        context.update({
#            'executors': User.objects.all(),
#            'labels': Label.objects.all(),
#            'selected_status': self.request.GET.get('status', ''),
#            'selected_executor': self.request.GET.get('executor', ''),
#            'selected_label': self.request.GET.get('labels', ''),
#            'self_tasks': self.request.GET.get('self_tasks', '') == 'on'
#        })
#        return context
    
#    def get_filterset_kwargs(self, filterset_class):
#        kwargs = super().get_filterset_kwargs(filterset_class)
#        kwargs['request'] = self.request
#        return kwargs

#    def get_context_data(self, **kwargs):
#        context = super().get_context_data(**kwargs)
#        context.update({
#            'executors': User.objects.all(),
#            'labels': Label.objects.all(),
#            'selected_status': self.request.GET.get('status', ''),
#            'selected_assigned_to': self.request.GET.get('assigned_to', ''),
#            'selected_label': self.request.GET.get('label', ''),
#            'self_tasks': self.request.GET.get('self_tasks', '') == 'on'
#        })
#        return context
    
#    def get_filterset_kwargs(self, filterset_class):
#        kwargs = super().get_filterset_kwargs(filterset_class)
#        kwargs['request'] = self.request
#        kwargs['data'] = self.request.GET
#        return kwargs


class TaskCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('tasks:list')
    success_message = _('Task created successfully!')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('tasks:list')
    success_message = _('Task updated successfully')


class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, 
                     SuccessMessageMixin, DeleteView):
    model = Task
    template_name = 'tasks/task_confirm_delete.html'
    success_url = reverse_lazy('tasks:list')
    success_message = _('Task deleted successfully')

    def test_func(self):
        task = self.get_object()
        return task.author == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, _('Only task author can delete it'))
        return redirect('tasks:list')


class TaskDetailView(DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'tasks/task_detail.html'
