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
    password1 = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput,
        required=True,
        help_text=_("Your password must contain at least 3 characters."),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput,
        required=True,
        help_text=_("Please enter your password again for verification."),
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('password', None)
        self.fields.pop('password_help_text', None)
    
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        
        if password1 and password1 != password2:
            self.add_error("password2", _(
                "The two password fields didn’t match."))
        
        if password1 and len(password1) < 3:
            self.add_error("password1", _(
                "Password must be at least 3 characters."))
        
        return cleaned_data
