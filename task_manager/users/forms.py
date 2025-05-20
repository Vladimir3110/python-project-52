from django import forms
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput, label=_("Password"),
        help_text=_("Your password must contain at least 3 characters."))
    password_confirm = forms.CharField(
        widget=forms.PasswordInput, label=_("Password confirmation"),
        help_text=_("Please enter your password again for verification."))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username']
        labels = {
            'first_name': _("First name"),
            'last_name': _("Last name"),
            'username': _("Username"),
        }
        help_texts = {
            'username': _(
                "Required. 150 characters or fewer. "
                "Letters, digits and @/./+/-/_ only."
            ),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        if password != password_confirm:
            raise forms.ValidationError_("The passwords do not match")
        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserUpdateForm(UserRegistrationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].required = False
        self.fields['password_confirm'].required = False

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')

        # Если введен новый пароль, обновляем его
        if password:
            user.set_password(password)

        user.first_name = self.cleaned_data.get('first_name', user.first_name)
        user.last_name = self.cleaned_data.get('last_name', user.last_name)

        if commit:
            user.save()

        return user
