from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordResetForm, AuthenticationForm
from .models import CustomUser


text_input_widget = forms.TextInput(attrs={
    'class': 'form-control bg-secondary bg-opacity-10 text-light border-secondary',
})

select_widget = forms.Select(attrs={
    'class': 'form-select bg-secondary bg-opacity-10 text-light border-secondary',
})

email_input_widget = forms.EmailInput(attrs={
    'class': 'form-control bg-secondary bg-opacity-10 text-light border-secondary',
    'placeholder': 'Enter your email',
})

password_input_widget = forms.PasswordInput(attrs={
    'class': 'form-control bg-secondary bg-opacity-10 text-light border-secondary',
    'autocomplete': 'new-password',
})

class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(
        widget=password_input_widget
    )

    password2 = forms.CharField(
        widget=password_input_widget
    )

    email = forms.EmailField(
        widget=email_input_widget
    )

    class Meta:
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('cefr_level',)
        widgets = {
            'username': text_input_widget,
            'cefr_level': select_widget
        }


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = UserChangeForm.Meta.fields


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'username': text_input_widget,
            'first_name': text_input_widget,
            'last_name': text_input_widget,
            'email': email_input_widget,
        }


class StyledPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        widget=email_input_widget
    )


class StyledLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=text_input_widget
    )

    password = forms.CharField(
        widget=password_input_widget
    )