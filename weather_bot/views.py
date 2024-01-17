import asyncio
from typing import Any
from django.db.models.query import QuerySet

from django.shortcuts import redirect
from django.views.generic import ListView

from main_bot import send_weather
from weather_bot.models import Profile


class HomeView(ListView):
    model = Profile
    template_name = 'weather_bot/home.html'
    context_object_name = 'profiles'


    def get_queryset(self):
        return Profile.objects.all()


def send_weather_in_moscow(request, profile_id):
    profile = Profile.objects.get(id=profile_id)
    asyncio.run(send_weather(profile.id_user, 'Moscow'))
    return redirect(profile.get_absolute_url())
