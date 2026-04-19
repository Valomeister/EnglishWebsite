from django.urls import path

from .views import DeckListView, DeckDetailView, HomeView
from .views import edit_deck_with_cards, create_deck_with_cards, delete_deck

urlpatterns = [
    path('', HomeView.as_view(), name = 'home'),
    path('decks/', DeckListView.as_view(), name = 'deck_list'),
    path('decks/<int:pk>/', DeckDetailView.as_view(), name = 'deck_detail'),
    path('decks/<int:pk>/edit/', edit_deck_with_cards, name = 'deck_edit'),
    path('decks/<int:pk>/delete/', delete_deck, name = 'deck_delete'),
    path('decks/create/', create_deck_with_cards, name = 'deck_create'),
]