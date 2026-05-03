import json
import math

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q, Prefetch, Sum, Value
from django.db.models.aggregates import Avg
from django.db.models.functions import Coalesce
from django.http import JsonResponse
from django.urls import reverse
from django.views.generic import ListView, DetailView, TemplateView
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .forms import DeckForm, DeckFormSet
from .models import Deck, Card, CardProgress


###########
# HOME #
###########

class HomeView(TemplateView):
    template_name = 'home.html'


###########
# DECKS #
###########


class DeckListView(LoginRequiredMixin, ListView):
    model = Deck
    template_name = 'deck_list.html'
    ordering = '-pk'

    def get_queryset(self):
        return Deck.objects.filter(author=self.request.user)


def get_mastery_options(last_inputs):
    good_inputs = last_inputs.count(3)
    bad_inputs = last_inputs.count(1)
    score = max(good_inputs - bad_inputs, 0)
    multiplier = score + 1
    mastery_options = [-math.ceil(5 / multiplier), 0, 5 * multiplier]

    return mastery_options

def mastery_options_to_strs(mastery_options):
    return [('+' if i >= 0 else '') + str(i) for i in mastery_options]

def get_cards_with_progress(request, deck):
    cards = Card.objects.filter(deck=deck).prefetch_related(
        Prefetch(
            'cardprogress_set',
            queryset=CardProgress.objects.filter(user=request.user),
            to_attr='user_progress'
        )
    )

    for card in cards:
        progress = card.user_progress[0] if card.user_progress else None

        if progress and progress.last_inputs:
            card.mastery_options = mastery_options_to_strs(get_mastery_options(progress.last_inputs))
        else:
            card.mastery_options = mastery_options_to_strs([-5, 0, 5])

    return cards


class DeckAssessView(LoginRequiredMixin, DetailView):
    model = Deck
    template_name = 'deck_assess.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cards'] = get_cards_with_progress(self.request, self.object)

        return context


class DeckStudyView(LoginRequiredMixin, DetailView):
    model = Deck
    template_name = 'deck_study.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cards'] = get_cards_with_progress(self.request, self.object)

        return context



@login_required
@require_POST
def update_progress(request, pk):
    deck = get_object_or_404(Deck, pk=pk)

    data = json.loads(request.body)
    card_id = data.get('card_id')
    option = data.get('option')
    mode = data.get('mode')
    reset = data.get('reset')

    if reset:
        CardProgress.objects.filter(user=request.user, card__deck=deck).delete()

        return JsonResponse({
            "success": True,
            "reset": True
        })
    else:
        card = get_object_or_404(Card, pk=card_id, deck=deck)
        progress, created = CardProgress.objects.update_or_create(
            user=request.user,
            card=card,
            create_defaults={
                'mastery': 0
            }
        )

        if mode == 'assess':
            mastery_options = [0, 50, 100]
            mastery = mastery_options[option - 1]
        else:
            last_inputs = progress.last_inputs or []
            mastery = progress.mastery or 0
            mastery_options = get_mastery_options(last_inputs)
            mastery += mastery_options[option - 1]
            mastery = max(0, min(99, mastery))

            last_inputs.append(option)
            progress.last_inputs = last_inputs[-5:]

        progress.mastery = mastery
        progress.save()

        return JsonResponse({
            'success': True,
            'mastery': mastery,
            'masteryOptions': mastery_options_to_strs(get_mastery_options(progress.last_inputs))
        })


class DeckDetailView(LoginRequiredMixin, DetailView):
    model = Deck
    template_name = 'deck_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        deck = self.object
        progress = CardProgress.objects.filter(card__deck=deck, user=self.request.user)
        total_cards = deck.cards.count()

        if progress.exists():
            total_mastery = progress.aggregate(
                total_mastery=Sum(Coalesce('mastery', Value(0)))
            )['total_mastery']

            context['progress'] = total_mastery / total_cards if total_cards else 0.0
            context['progress_exists'] = True
        else:
            context['progress'] = 0.0
            context['progress_exists'] = False

        context['cards'] = get_cards_with_progress(self.request, deck)

        return context


@login_required
def edit_deck_with_cards(request, pk):
    deck = get_object_or_404(Deck, pk=pk, author=request.user)
    queryset = Card.objects.filter(deck=pk).order_by("id")

    if request.method == 'POST':
        form = DeckForm(request.POST, instance=deck)
        formset = DeckFormSet(request.POST, queryset=queryset)
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
        formset = DeckFormSet(queryset=queryset)

    print(form.errors)
    print(formset.errors)

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
        formset = DeckFormSet(request.POST, queryset=Card.objects.none())
        if form.is_valid() and formset.is_valid():
            form.save()
            instances = formset.save(commit=False)
            for instance in instances:
                instance.deck = deck
                instance.save()
            return redirect('deck_detail', pk=deck.id)

    else:
        form = DeckForm(instance=deck)
        formset = DeckFormSet(queryset=Card.objects.none())

    return render(request, 'deck_create.html', {
        'form': form,
        'formset': formset,
    })


@require_POST
def delete_deck(request, pk):
    deck = get_object_or_404(Deck, pk=pk, author=request.user)
    deck.delete()

    return redirect('deck_list')

###########
# LIBRARY #
###########

class LibraryListView(ListView):
    model = Deck
    template_name = 'deck_library.html'

    def get_queryset(self):
        qs = Deck.objects.all().annotate(
            cards_count=Count("cards")
        ).order_by('id')

        levels = self.request.GET.getlist("level")
        min_words = self.request.GET.get("min_words")
        max_words = self.request.GET.get("max_words")

        if levels:
            q = Q()

            real_levels = [x for x in levels if x != "None"]

            if real_levels:
                q |= Q(cefr_level__in=real_levels)

            if "None" in levels:
                q |= Q(cefr_level__isnull=True) | Q(cefr_level="")

            qs = qs.filter(q)

        if min_words:
            qs = qs.filter(cards_count__gte=min_words)

        if max_words:
            qs = qs.filter(cards_count__lte=max_words)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cefr_levels'] = list(Deck.CEFR_LEVEL_CHOICES.keys())
        context["selected_levels"] = self.request.GET.getlist("level")

        return context


@login_required
@require_POST
def toggle_starred(request, pk):
    deck = get_object_or_404(Deck, pk=pk)

    if deck.starred_by.filter(pk=request.user.pk).exists():
        deck.starred_by.remove(request.user)
        starred = False
    else:
        deck.starred_by.add(request.user)
        starred = True

    return JsonResponse({
        "starred": starred,
        "count": deck.starred_by.count(),
    })