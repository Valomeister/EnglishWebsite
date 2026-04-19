from django.contrib.auth.views import PasswordResetView, LoginView
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin

from .forms import CustomUserCreationForm, UserUpdateForm, StyledPasswordResetForm, StyledLoginView
from .models import CustomUser

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


class AccountDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = CustomUser
    template_name = 'account_detail.html'

    def test_func(self):
        return self.get_object() == self.request.user


class AccountEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = CustomUser
    form_class = UserUpdateForm
    template_name = 'account_edit.html'

    def test_func(self):
        return self.get_object() == self.request.user


class CustomPasswordResetView(PasswordResetView):
    form_class = StyledPasswordResetForm
    template_name = 'registration/password_reset_form.html'


class CustomLoginView(LoginView):
    form_class = StyledLoginView
    template_name = 'registration/login.html'
