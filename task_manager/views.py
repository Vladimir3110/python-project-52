# from django.contrib import messages
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'task_manager/index.html'
