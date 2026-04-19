from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordResetForm, AuthenticationForm
from .models import CustomUser



class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control bg-secondary bg-opacity-10 text-light border-secondary',
            'autocomplete': 'new-password',
        })
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control bg-secondary bg-opacity-10 text-light border-secondary',
            'autocomplete': 'new-password',
        })
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control bg-secondary bg-opacity-10 text-light border-secondary',
            'placeholder': 'Enter your email',
        })
    )

    class Meta:
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('cefr_level',)
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control bg-secondary bg-opacity-10 text-light border-secondary'
            }),
            'cefr_level': forms.Select(attrs={
                'class': 'form-select bg-secondary bg-opacity-10 text-light border-secondary',
            }),
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
            'username': forms.TextInput(attrs={
                'class': 'form-control bg-secondary bg-opacity-10 text-light border-secondary',
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control bg-secondary bg-opacity-10 text-light border-secondary',
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control bg-secondary bg-opacity-10 text-light border-secondary'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control bg-secondary bg-opacity-10 text-light border-secondary'
            })
        }


class StyledPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control bg-secondary bg-opacity-10 text-light border-secondary',
            'placeholder': 'Enter your email',
        })
    )


class StyledLoginView(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control bg-secondary bg-opacity-10 text-light border-secondary',
        })
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control bg-secondary bg-opacity-10 text-light border-secondary',
        })
    )