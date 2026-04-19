from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse_lazy


class CustomUser(AbstractUser):
    CEFR_LEVEL_CHOICES = {
        'A1': 'Beginner',
        'A2': 'Elementary',
        'B1': 'Intermediate',
        'B2': 'Upper-Intermediate',
        'C1': 'Advanced',
        'C2': 'Proficiency',
    }
    cefr_level = models.CharField(max_length=10, choices=CEFR_LEVEL_CHOICES, null=True, blank=True)

    def get_absolute_url(self):
        print(f'{self.pk = }')
        return reverse_lazy('account', kwargs={'pk': self.pk})
