from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
import statistics
from django.shortcuts import reverse


class Card(models.Model):
    title = models.CharField('card title', max_length=100, unique=True)
    body = models.TextField('idea')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True)
    mod_date = models.DateTimeField(auto_now=True)
    rating_enable = models.BooleanField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('cards:card-detail', kwargs={'pk': self.pk})

    def count_ratings(self):
        ratings = CardRating.objects.filter(card=self)
        return len(ratings)

    def get_avg_ratings(self):
        ratings = CardRating.objects.filter(card=self)
        if ratings:
            return round(statistics.mean([rating.stars for rating in ratings]))
        else:
            return 0


class CardRating(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    star_from_user = models.ForeignKey(User, on_delete=models.CASCADE)
    stars = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], default=0)

    def __str__(self):
        return f'Rating for {self.card.title}'

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['card', 'star_from_user'], name='vote_constraint'),
        ]
