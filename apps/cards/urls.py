from django.urls import path, include
from rest_framework import routers

from . import views

app_name = 'cards'

router = routers.DefaultRouter()
router.register('card', views.CardAPIView)
router.register('rating', views.CardRatingAPIView)

urlpatterns = [
    path('', views.CardListView.as_view(), name='card-list'),
    path('new/', views.CardCreateView.as_view(), name='card-add'),
    path('<int:pk>/detail/', views.CardDetailView.as_view(), name='card-detail'),
    path('<int:pk>/update', views.CardUpdateView.as_view(), name='card-update'),
    path('<int:pk>/delete/', views.CardDeleteView.as_view(), name='card-delete'),
    path('user/<str:username>/', views.UserCardListView.as_view(), name='user-cards'),
    path('<int:pk>/add-rating/', views.CardRatingView.as_view(), name='add-rating'),
    # path('api/', include(router.urls)),   # todo uncomment this line for use django REST API
]
