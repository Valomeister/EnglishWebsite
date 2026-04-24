from django import forms
from django.forms import modelformset_factory
from .models import Deck, Card


from django import forms


def text_widget_factory(semibold=False, fs=None, placeholder=None):
    classes = [
        'form-control',
        'bg-transparent',
        'bg-opacity-10',
        'text-light',
        'border-secondary',
        'border-0',
        'border-bottom',
        'rounded-0',
        'p-0',
        'fw-semibold' if semibold else '',
        fs if fs else '',
    ]

    attrs = {
        'class': ' '.join(classes),
        'autocomplete': 'off'
    }

    if placeholder:
        attrs['placeholder'] = placeholder

    return forms.TextInput(attrs=attrs)

text_input_widget = forms.TextInput(attrs={
    'class': 'form-control bg-secondary bg-opacity-10 text-light border-secondary',
})

select_widget = forms.Select(attrs={
    'class': 'form-select bg-secondary bg-opacity-10 text-light border-secondary',
})


class DeckForm(forms.ModelForm):
    class Meta:
        model = Deck
        fields = ['title', 'description', 'cefr_level']
        widgets = {
            'title': text_widget_factory(semibold=True, fs='fs-4', placeholder='Enter title'),
            'description': text_widget_factory(placeholder='Description'),
            'cefr_level': select_widget,
        }


DeckFormSet = modelformset_factory(Card, fields=['word', 'translation', 'description'], can_delete=True, extra=0, widgets={
    'word': text_widget_factory(semibold=True, fs='fs-4', placeholder='Enter word'),
    'translation': text_widget_factory(placeholder='Translation'),
    'description': forms.Textarea(attrs={
        'class': 'form-control bg-secondary bg-opacity-10 text-light rounded-0 border-0',
        'placeholder': 'Description (optional)'
    })
})
