from django.urls import path
from django.views.generic import TemplateView

app_name = 'home_page'
urlpatterns = [
    path('', TemplateView.as_view(template_name='home_page/home_page.html'), name='home-page')
]
