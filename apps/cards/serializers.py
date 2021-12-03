from rest_framework import serializers

from .models import Card, CardRating


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = [
            'id',
            'title',
            'body',
            'author',
            'pub_date',
            'mod_date',
            'rating_enable',
            'count_ratings',
            'get_avg_ratings',
        ]


class CardRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = CardRating
        fields = ['id', 'card', 'star_from_user', 'stars']
