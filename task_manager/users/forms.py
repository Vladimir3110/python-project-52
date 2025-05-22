from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.utils.translation import gettext_lazy as _

from task_manager.users.models import User


class CustomUsersCreateForm(UserCreationForm):
    password1 = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput,
        help_text=_("Your password must contain at least 3 characters."),
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 
                  'password1', 'password2']
        labels = {
            'first_name': _("First name"),
            'last_name': _("Last name"),
            'username': _("Username"),
            'password1': _("Password"),
            'password2': _("Password confirmation"),
        }
        help_texts = {
            'username': _(
                "Required. 150 characters or fewer. "
                "Letters, digits and @/./+/-/_ only."
            ),
            'password1': _("Your password must contain at least 3 characters.")
        }


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
