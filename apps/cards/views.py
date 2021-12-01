from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView, RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.db.models import Avg

from .models import Card, CardRating


class CardListView(ListView):
    model = Card
    context_object_name = 'cards'
    ordering = ['?']
    paginate_by = 9


class CardCreateView(LoginRequiredMixin, CreateView):
    model = Card
    fields = ['title', 'body', 'rating_enable']
    login_url = 'users:login'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class CardDetailView(DetailView):
    model = Card

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if str(self.request.user) != 'AnonymousUser':
            user_review = CardRating.objects.filter(card_id=self.kwargs['pk'], star_from_user=self.request.user)
            if user_review:
                context['user_review'] = user_review.get().stars
        return context


class CardUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Card
    fields = ['title', 'body', 'rating_enable']
    login_url = 'users:login'

    def form_valid(self, form):
        form.instance.author = form.instance.author
        return super().form_valid(form)

    def test_func(self):
        card = self.get_object()
        if any([self.request.user == card.author, self.request.user.is_superuser]) and card.count_ratings() < 6:
            return True
        return False


class CardDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Card
    success_url = reverse_lazy('cards:card-list')
    login_url = 'users:login'

    def test_func(self):
        card = self.get_object()
        if any([self.request.user == card.author, self.request.user.is_superuser]):
            return True
        return False


class UserCardListView(ListView):
    model = Card
    context_object_name = 'cards'
    paginate_by = 9

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Card.objects.filter(author=user).order_by('-pub_date')


class CardRatingView(LoginRequiredMixin, UserPassesTestMixin, RedirectView):
    login_url = 'users:login'
    redirect_field_name = 'home_page:home_page'

    def test_func(self):
        card = Card.objects.get(id=self.kwargs['pk'])
        if any([self.request.user == card.author, self.request.user.is_superuser, card.rating_enable is False]):
            return False
        return True

    def get_redirect_url(self, *args, **kwargs):
        user_review = CardRating.objects.filter(card_id=self.kwargs['pk'], star_from_user=self.request.user)
        user = self.request.user
        if self.request.method == 'POST':
            rating = self.request.POST['rating']
            if user_review:
                user_review.update(stars=rating)
            else:
                CardRating.objects.create(card_id=kwargs['pk'], star_from_user=user, stars=rating)
            return reverse('cards:card-detail', kwargs={'pk': kwargs['pk']})


class SortCardListView(ListView):
    model = Card
    context_object_name = 'cards'
    paginate_by = 9

    def get_queryset(self):
        filter_by = self.request.GET['filter']
        cards_avg = Card.objects.annotate(average_stars=Avg('cardrating__stars'))
        all_cards = Card.objects.all()
        best_ideas = cards_avg.order_by('-average_stars')
        worst_ideas = cards_avg.order_by('average_stars')
        newest_cards = all_cards.order_by('-pub_date')
        oldest_cards = all_cards.order_by('pub_date')
        gt_one_star = cards_avg.filter(average_stars__gt=1)
        gt_two_star = cards_avg.filter(average_stars__gt=2)
        gt_three_star = cards_avg.filter(average_stars__gt=3)
        gt_fore_star = cards_avg.filter(average_stars__gt=4)
        eq_five_star = cards_avg.filter(average_stars=5)
        filters = {
            'best_ideas': best_ideas,
            'worst_ideas': worst_ideas,
            'newest_cards': newest_cards,
            'oldest_cards': oldest_cards,
            'gt_one_star': gt_one_star,
            'gt_two_star': gt_two_star,
            'gt_three_star': gt_three_star,
            'gt_fore_star': gt_fore_star,
            'eq_five_star': eq_five_star,
        }
        context = filters[filter_by]
        return context
