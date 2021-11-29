from django.views.generic.list import ListView

from .models import Card


class CardListView(ListView):
    model = Card
    context_object_name = 'cards'
    ordering = ['-pub_date']
