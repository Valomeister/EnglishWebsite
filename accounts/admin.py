from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = [
        "email",
        "username",
        "cefr_level",
        "is_staff",
    ]
    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("cefr_level",)}),)
    add_fieldsets = UserAdmin.add_fieldsets + ((None, {"fields": ("cefr_level",)}),)

admin.site.register(CustomUser, CustomUserAdmin)

