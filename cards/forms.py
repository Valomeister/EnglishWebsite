from django import forms
from django.forms import modelformset_factory
from .models import Deck, Card


class DeckForm(forms.ModelForm):
    class Meta:
        model = Deck
        fields = ['title', 'description', 'cefr_level']


DeckFormSet = modelformset_factory(Card, fields=['word', 'translation', 'description'], can_delete=True, extra=0)
DeckFormSetExtra = modelformset_factory(Card, fields=['word', 'translation', 'description'], can_delete=True, extra=1)
