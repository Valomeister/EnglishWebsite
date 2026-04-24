from django.db import models
from accounts.models import CustomUser


class Deck(models.Model):
    CEFR_LEVEL_CHOICES = {
        'A1': 'Beginner',
        'A2': 'Elementary',
        'B1': 'Intermediate',
        'B2': 'Upper-Intermediate',
        'C1': 'Advanced',
        'C2': 'Proficiency',
    }
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    cefr_level = models.CharField(max_length=10, choices=CEFR_LEVEL_CHOICES, null=True, blank=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='decks', default=1)

    def __str__(self):
        return f'{self.title} ({self.cefr_level})'

    class Meta:
        ordering = ['id']


class Card(models.Model):
    word = models.CharField(max_length=200)
    translation = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE, related_name='cards')

    def __str__(self):
        return f'{self.word} - {self.translation}'

    class Meta:
        ordering = ['id']