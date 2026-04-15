from django.contrib import admin

from .models import Topic, Deck, Card


class DeckInline(admin.TabularInline):
    model = Deck
    extra = 1


class TopicAdmin(admin.ModelAdmin):
    inlines = [
        DeckInline,
    ]
    list_display = [
        'name'
    ]


class CardInline(admin.TabularInline):
    model = Card
    extra = 1

class DeckAdmin(admin.ModelAdmin):
    inlines = [
        CardInline,
    ]
    list_display = [
        'title',
        'cefr_level',
    ]

admin.site.register(Topic, TopicAdmin)
admin.site.register(Deck, DeckAdmin)
