from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Card(models.Model):
    title = models.CharField('card title', max_length=100, unique=True)
    body = models.TextField('idea')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True)
    mod_date = models.DateTimeField(auto_now=True)
    rating_enable = models.BooleanField()

    def __str__(self):
        return self.title


class CardRating(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    star_from_user = models.ForeignKey(User, on_delete=models.CASCADE)
    stars = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], default=0)

    def __str__(self):
        return f'Rating for {self.card.title}'
