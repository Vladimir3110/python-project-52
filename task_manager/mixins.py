from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import redirect_to_login
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _


class AuthRequiredMixin(LoginRequiredMixin):
    """Миксин для проверки авторизации с кастомными сообщениями"""
    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            messages.error(self.request, 
                           _("You are not logged in! Please sign in.")
                           )
            return redirect_to_login(
                self.request.get_full_path(),
                login_url=reverse(settings.LOGIN_URL)
                )
        return super().handle_no_permission()


class OwnerCheckMixin(UserPassesTestMixin):
    """Миксин для проверки владения объектом"""
    error_message = _("You do not have permission to modify another user.")
    error_redirect = reverse_lazy('user_list')

    def test_func(self):
        return self.request.user.id == self.get_object().id

    def handle_no_permission(self):
        messages.error(self.request, self.error_message)
        return redirect(self.error_redirect)


class ProtectedDeleteMixin:
    """Миксин для защиты от удаления используемых объектов"""
    protected_message = _("Cannot delete user because it is in use")
    protected_redirect = None

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        if self.check_protected_condition(obj):
            messages.error(request, 
                           self.protected_message, 
                           extra_tags='alert alert-danger')
            return redirect(self.protected_redirect)
        return super().post(request, *args, **kwargs)

    def check_protected_condition(self, obj):
        raise NotImplementedError
