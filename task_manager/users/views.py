from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

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
    success_message = "Пользователь успешно зарегистрирован"


# Редактирование пользователя
class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'users/user_update.html'
    success_url = reverse_lazy('user_list')

    def test_func(self):
        return self.request.user.id == self.get_object().id

    def handle_no_permission(self):
        messages.error(
            self.request,
            "У вас нет прав для изменения другого пользователя.",
            extra_tags='error'
        )
        return redirect(self.success_url)

    def form_valid(self, form):
        response = super().form_valid(form)      
        # Если пароль был изменен, обновляем сессию
        if 'password' in form.cleaned_data and form.cleaned_data['password']:
            update_session_auth_hash(self.request, self.object)
        messages.success(
            self.request, 
            "Пользователь успешно изменен",
            extra_tags='success'
        )
        return response


# Удаление пользователя
class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = User
    template_name = 'users/user_confirm_delete.html'
    success_url = reverse_lazy('user_list')

    def test_func(self):
        return self.request.user.id == self.get_object().id

    def handle_no_permission(self):
        messages.error(
            self.request,
            "У вас нет прав для изменения другого пользователя.",
            extra_tags='alert-danger'
        )
        return redirect(self.success_url)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()

        messages.success(self.request, "Пользователь успешно удален")
        return redirect(self.success_url)


# Вход
class UserLoginView(LoginView):
    template_name = 'users/login.html'

    def form_valid(self, form):
        messages.success(self.request, "Вы залогинены")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('index')


# Выход
class UserLogoutView(LogoutView):
    next_page = reverse_lazy('index')

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        messages.success(request, "Вы разлогинены")
        return response
