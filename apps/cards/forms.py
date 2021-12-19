from django import forms


class CardFilterForm(forms.Form):
    NEWEST_CARD = '11'
    OLDEST_CARD = '12'
    BEST_IDEA = '13'
    WORST_IDEA = '14'
    MORE_ONE = '21'
    MORE_TWO = '22'
    MORE_TREE = '23'
    MORE_FOUR = '24'
    EQUAL_ONE = '31'
    EQUAL_TWO = '32'
    EQUAL_THREE = '33'
    EQUAL_FOUR = '34'
    EQUAL_FIVE = '35'

    FILTER_BY = (
        ('', 'Choose'),
        ('By card', (
            (NEWEST_CARD, 'Newest cards'),
            (OLDEST_CARD, 'Oldest cards'),
        )
         ),
        ('By idea', (
            (BEST_IDEA, 'Best ideas'),
            (WORST_IDEA, 'Worst ideas'),
        )
         ),
        ('By rating', (
            (MORE_ONE, 'More than 1 star'),
            (MORE_TWO, 'More than 2 stars'),
            (MORE_TREE, 'More than 3 stars'),
            (MORE_FOUR, 'More than 4 stars'),
        )
         ),
        ('By stars', (
            (EQUAL_ONE, 'Equal 1 stars'),
            (EQUAL_TWO, 'Equal 2 stars'),
            (EQUAL_THREE, 'Equal 3 stars'),
            (EQUAL_FOUR, 'Equal 4 stars'),
            (EQUAL_FIVE, 'Equal 5 stars'),
        ))
    )

    filter = forms.ChoiceField(choices=FILTER_BY, widget=forms.Select(attrs={'class': 'form-select'}))
