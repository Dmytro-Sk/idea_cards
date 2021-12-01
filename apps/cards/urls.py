from django.urls import path

from . import views

app_name = 'cards'
urlpatterns = [
    path('', views.CardListView.as_view(), name='card-list'),
    path('new/', views.CardCreateView.as_view(), name='card-add'),
    path('<int:pk>/detail/', views.CardDetailView.as_view(), name='card-detail'),
    path('<int:pk>/update', views.CardUpdateView.as_view(), name='card-update'),
    path('<int:pk>/delete/', views.CardDeleteView.as_view(), name='card-delete'),
    path('user/<str:username>/', views.UserCardListView.as_view(), name='user-cards'),
    path('<int:pk>/add-rating/', views.CardRatingView.as_view(), name='add-rating'),
    path('sortby/', views.SortCardListView.as_view(), name='card-sortby'),
]
