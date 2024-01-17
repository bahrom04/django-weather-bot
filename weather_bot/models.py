from django.db import models
from django.urls import reverse


class Profile(models.Model):
    id_user = models.IntegerField()
    first_name = models.CharField(max_length=50)
    nickname = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f'{self.id_user} - {self.first_name} - {self.nickname}'

    def get_absolute_url(self):
        return reverse('weather_bot:home')

    class Meta:
        db_table = 'users'
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'
        ordering = ['first_name']
