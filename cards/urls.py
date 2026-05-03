from django.urls import path

from .views import (DeckListView, DeckDetailView, HomeView, LibraryListView, DeckAssessView, DeckStudyView,
                    edit_deck_with_cards, create_deck_with_cards, delete_deck, toggle_starred, update_progress)

urlpatterns = [
    path('', HomeView.as_view(), name = 'home'),

    path('decks/library/', LibraryListView.as_view(), name='deck_library'),
    path('decks/library/<int:pk>/star/', toggle_starred, name='toggle_starred'),

    path('decks/mydecks/', DeckListView.as_view(), name = 'deck_list'),
    path('decks/<int:pk>/', DeckDetailView.as_view(), name = 'deck_detail'),
    path('decks/<int:pk>/edit/', edit_deck_with_cards, name = 'deck_edit'),
    path('decks/<int:pk>/delete/', delete_deck, name = 'deck_delete'),
    path('decks/create/', create_deck_with_cards, name = 'deck_create'),
    path('decks/<int:pk>/assess/', DeckAssessView.as_view(), name = 'deck_assess'),
    path('decks/<int:pk>/study/', DeckStudyView.as_view(), name = 'deck_study'),
    path('decks/<int:pk>/study/progress/', update_progress, name = 'study_progress'),
]