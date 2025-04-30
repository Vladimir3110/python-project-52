from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from task_manager.mixins import (
    AuthRequiredMixin,
    OwnerCheckMixin,
    ProtectedDeleteMixin,
)

from .forms import UserRegistrationForm, UserUpdateForm


# Список пользователей
class UserListView(ListView):
    model = User
    template_name = 'users/user_list.html'
    context_object_name = 'users'


class UserCreateView(SuccessMessageMixin, CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('login')
    success_message = _("User successfully registered")


# Редактирование пользователя
class UserUpdateView(AuthRequiredMixin, OwnerCheckMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'users/user_update.html'
    success_url = reverse_lazy('user_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        if 'password' in form.cleaned_data and form.cleaned_data['password']:
            update_session_auth_hash(self.request, self.object)
        messages.success(self.request, _("User successfully changed"))
        return response


# Удаление пользователя
class UserDeleteView(
    AuthRequiredMixin, OwnerCheckMixin, ProtectedDeleteMixin, DeleteView):
    model = User
    template_name = 'users/user_confirm_delete.html'
    success_url = reverse_lazy('user_list')
    protected_redirect = success_url

    def check_protected_condition(self, user):
        return user.authored_tasks.exists() or user.assigned_tasks.exists()

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        messages.success(request, _("User deleted successfully"))
        return response


# Вход
class UserLoginView(LoginView):
    template_name = 'users/login.html'

    def form_valid(self, form):
        messages.success(self.request, _("You are logged in"))
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('index')


# Выход
class UserLogoutView(LogoutView):
    next_page = reverse_lazy('index')

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        messages.success(request, _("You are logged out"))
        return response
