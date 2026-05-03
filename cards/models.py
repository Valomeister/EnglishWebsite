from doctest import master

from django.core.validators import MinValueValidator, MaxValueValidator
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
    starred_by = models.ManyToManyField(CustomUser, related_name='starred_decks', null=True, blank=True)

    def __str__(self):
        return f'{self.title} ({self.cefr_level})'

    class Meta:
        ordering = ['id']


class Card(models.Model):
    word = models.CharField(max_length=200)
    translation = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE, related_name='cards')
    users = models.ManyToManyField(CustomUser, through='CardProgress',  related_name='cards_progress')

    def __str__(self):
        return f'{self.word} - {self.translation}'

    class Meta:
        ordering = ['id']


class CardProgress(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)

    mastery = models.SmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    last_inputs = models.JSONField(default=list)

    def __str__(self):
        return f'{self.user.username} <-> {self.card.word} | {self.mastery} | {self.last_inputs}'

    class Meta:
        unique_together = ('user', 'card')