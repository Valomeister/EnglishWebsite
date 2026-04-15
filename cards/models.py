from django.db import models


class Topic(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return  self.name


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
    description = models.TextField()
    cefr_level = models.CharField(max_length=10, choices=CEFR_LEVEL_CHOICES, null=True, blank=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='topics')

    def __str__(self):
        return f'{self.title} ({self.cefr_level})'


class Card(models.Model):
    word = models.CharField(max_length=200)
    translation = models.CharField(max_length=200)
    description = models.TextField()
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE, related_name='cards')

    def __str__(self):
        return f'{self.word} - {self.translation}'