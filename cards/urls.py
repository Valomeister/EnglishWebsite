from django.urls import path

from .views import DeckListView, DeckDetailView
from .views import edit_deck_with_cards, create_deck_with_cards

urlpatterns = [
    path('', DeckListView.as_view(), name = 'deck_list'),
    path('<int:pk>/', DeckDetailView.as_view(), name = 'deck_detail'),
    path('<int:pk>/edit/', edit_deck_with_cards, name = 'deck_edit'),
    path('  create/', create_deck_with_cards, name = 'deck_create'),
]