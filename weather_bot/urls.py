from django.urls import path

from . import views
from .views import HomeView

app_name = 'weather_bot'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('send_weather/<int:profile_id>/',
         views.send_weather_in_moscow, name='send_weather'),
]
