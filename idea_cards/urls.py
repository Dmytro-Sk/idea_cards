from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.home_page.urls')),
    path('users/', include('apps.users.urls')),
    path('cards/', include('apps.cards.urls')),
    path('accounts/', include('allauth.urls')),
]
