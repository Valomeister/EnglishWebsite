from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q
from django.http import JsonResponse
from django.views.generic import ListView, DetailView, TemplateView
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .forms import DeckForm, DeckFormSet
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