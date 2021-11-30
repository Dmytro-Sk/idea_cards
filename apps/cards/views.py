from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from .models import Card


class CardListView(ListView):
    model = Card
    context_object_name = 'cards'
    ordering = ['-pub_date']


class CardCreateView(LoginRequiredMixin, CreateView):
    model = Card
    fields = ['title', 'body', 'rating_enable']
    login_url = 'users:login'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class CardDetailView(DetailView):
    model = Card


class CardUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Card
    fields = ['title', 'body', 'rating_enable']
    login_url = 'users:login'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if any([self.request.user == post.author, self.request.user.is_superuser]):
            return True
        return False


class CardDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Card
    success_url = reverse_lazy('cards:card-list')
    login_url = 'users:login'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class UserCardListView(ListView):
    model = Card
    template_name = 'cards/user_cards.html'
    context_object_name = 'cards'

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Card.objects.filter(author=user).order_by('-pub_date')
