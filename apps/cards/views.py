from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView, RedirectView
from django.views.generic.edit import FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.db.models import Avg
from rest_framework import viewsets

from .serializers import CardSerializer, CardRatingSerializer
from .models import Card, CardRating
from .forms import CardFilterForm


class CardListView(FormMixin, ListView):
    model = Card
    context_object_name = 'cards'
    paginate_by = 9
    form_class = CardFilterForm

    def get_queryset(self):
        if self.request.GET.get('filter'):
            filter_by = self.request.GET.get('filter')
            if filter_by == CardFilterForm.NEWEST_CARD:
                return Card.objects.all().order_by('-pub_date')
            elif filter_by == CardFilterForm.OLDEST_CARD:
                return Card.objects.all().order_by('pub_date')
            elif filter_by == CardFilterForm.BEST_IDEA:
                return Card.objects.annotate(average_stars=Avg('cardrating__stars')).order_by('-average_stars')
            elif filter_by == CardFilterForm.WORST_IDEA:
                return Card.objects.annotate(average_stars=Avg('cardrating__stars')).order_by('average_stars')
            elif filter_by[0] == '2':
                stars = filter_by[-1]
                return Card.objects.annotate(average_stars=Avg('cardrating__stars')).filter(average_stars__gt=stars)
            elif filter_by[0] == '3':
                stars = filter_by[-1]
                return Card.objects.annotate(average_stars=Avg('cardrating__stars')).filter(average_stars=stars)
        else:
            return Card.objects.all().order_by('-pub_date')


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


class CardAPIView(viewsets.ModelViewSet):
    queryset = Card.objects.all()
    serializer_class = CardSerializer


class CardRatingAPIView(viewsets.ModelViewSet):
    queryset = CardRating.objects.all()
    serializer_class = CardRatingSerializer
