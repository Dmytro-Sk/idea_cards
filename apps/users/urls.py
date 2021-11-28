from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from rest_framework import routers

from . import views

app_name = 'users'

router = routers.DefaultRouter()
router.register('api', views.UserAPIView)

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', include(router.urls)),
]
