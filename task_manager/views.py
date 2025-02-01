from django.contrib import messages
from django.views.generic.base import TemplateView


class IndexView(TemplateView):
    template_name = 'task_manager/index.html'

    def get(self, request, *args, **kwargs):
        messages.success(request, 'Добро пожаловать в Task Manager!')
        return super().get(request, *args, **kwargs)
