from django import forms
from django.forms import formset_factory, modelformset_factory
from .models import Deck, Card


class DeckForm(forms.ModelForm):
    class Meta:
        model = Deck
        fields = ['title', 'description']


DeckFormSet = modelformset_factory(Card, fields=['word', 'translation', 'description'], can_delete=True, extra=0)
