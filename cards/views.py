from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, TemplateView
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .forms import DeckForm, DeckFormSet, DeckFormSetExtra
from .models import Deck, Card


class HomeView(TemplateView):
    template_name = 'home.html'


class DeckListView(LoginRequiredMixin, ListView):
    model = Deck
    template_name = 'deck_list.html'
    ordering = '-pk'

    def get_queryset(self):
        return Deck.objects.filter(author=self.request.user)


class DeckDetailView(LoginRequiredMixin, DetailView):
    model = Deck
    template_name = 'deck_detail.html'


@login_required
def edit_deck_with_cards(request, pk):
    deck = get_object_or_404(Deck, pk=pk, author=request.user)

    if request.method == 'POST':
        form = DeckForm(request.POST, instance=deck)
        formset = DeckFormSet(request.POST, queryset=Card.objects.filter(deck=pk))
        if form.is_valid() and formset.is_valid():
            form.save()
            instances = formset.save(commit=False)
            for instance in instances:
                instance.deck = deck
                instance.save()
            for obj in formset.deleted_objects:
                obj.delete()
            return redirect('deck_detail', pk=deck.id)

    else:
        form = DeckForm(instance=deck)
        formset = DeckFormSet(queryset=Card.objects.filter(deck=pk))

    return render(request, 'deck_edit.html', {
        'form': form,
        'formset': formset,
        'pk': pk
    })


@login_required
def create_deck_with_cards(request):
    deck = Deck(author=request.user)

    if request.method == 'POST':
        form = DeckForm(request.POST, instance=deck)
        formset = DeckFormSetExtra(request.POST, queryset=Card.objects.none())
        if form.is_valid() and formset.is_valid():
            form.save()
            instances = formset.save(commit=False)
            for instance in instances:
                instance.deck = deck
                instance.save()
            return redirect('deck_detail', pk=deck.id)

    else:
        form = DeckForm(instance=deck)
        formset = DeckFormSetExtra(queryset=Card.objects.none())

    return render(request, 'deck_create.html', {
        'form': form,
        'formset': formset,
    })


@require_POST
def delete_deck(request, pk):
    deck = get_object_or_404(Deck, pk=pk, author=request.user)
    deck.delete()

    return redirect('deck_list')