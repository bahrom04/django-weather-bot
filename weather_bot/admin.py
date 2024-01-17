from django.contrib import admin

from weather_bot.models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id_user', 'first_name', 'nickname')
    list_display_links = ('id_user', 'first_name', 'nickname')
    search_fields = ('id_user', 'first_name', 'nickname')
