from django import forms
from django.contrib.auth.models import User


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput, label="Пароль",
        help_text="Ваш пароль должен содержать как минимум 3 символа.")
    password_confirm = forms.CharField(
        widget=forms.PasswordInput, label="Подтверждение пароля",
        help_text="Для подтверждения введите, пожалуйста, пароль ещё раз.")

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username']
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'username': 'Имя пользователя',
        }
        help_texts = {
            'username': "Обязательное поле. Не более 150 символов. \
            Только буквы, цифры и символы @/./+/-/_.",
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        if password != password_confirm:
            raise forms.ValidationError("Пароли не совпадают")
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
