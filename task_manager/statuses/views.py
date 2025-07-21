# from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin

# from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from task_manager.mixins import ProtectedDeleteMixin

from .forms import StatusForm
from .models import Status


class StatusListView(LoginRequiredMixin, ListView):
    model = Status
    template_name = 'statuses/status_list.html'
    context_object_name = 'statuses'


class StatusCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Status
    form_class = StatusForm
    template_name = 'statuses/status_form.html'
    success_url = reverse_lazy('status_list')
    success_message = _("Status successfully created")


class StatusUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Status
    form_class = StatusForm
    template_name = 'statuses/status_form.html'
    success_url = reverse_lazy('status_list')
    success_message = _("Status successfully updated")


# class StatusDeleteView(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
#    model = Status
#    template_name = 'statuses/status_confirm_delete.html'
#    success_url = reverse_lazy('status_list')
#    success_message = _("Status successfully deleted")

#    def delete(self, request, *args, **kwargs):
#        self.object = self.get_object()
        
#        if self.object.tasks.exists(): 
#            messages.error(
#                request,
#                _("Cannot delete status in use"),
#                extra_tags='alert-danger'
#            )
#            return redirect(self.success_url)
        
#        return super().delete(request, *args, **kwargs)

class StatusDeleteView(ProtectedDeleteMixin, 
                       SuccessMessageMixin, 
                       LoginRequiredMixin, 
                       DeleteView):
    model = Status
    template_name = 'statuses/status_confirm_delete.html'
    success_url = reverse_lazy('status_list')
    success_message = _("Status successfully deleted")
    protected_message = _("Cannot delete status because it is in use")
    protected_redirect = success_url

    def check_protected_condition(self, obj):
        return obj.tasks.exists()
