from django import forms
from django.forms import formset_factory, modelformset_factory
from .models import Deck, Card


class DeckForm(forms.ModelForm):
    class Meta:
        model = Deck
        fields = ['title', 'description']


DeckFormSet = modelformset_factory(Card, fields=['word', 'translation', 'description'], can_delete=True, extra=1)



# from django import forms
# from django.forms import inlineformset_factory
# from .models import Deck, Card
#
#
# class DeckForm(forms.ModelForm):
#     class Meta:
#         model = Deck
#         fields = ['title', 'description']
#
#
# CardFormSet = inlineformset_factory(
#     Deck,
#     Card,
#     fields=['word', 'translation', 'description'],
#     extra=1,
#     can_delete=True,
# )