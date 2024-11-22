from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.timezone import now


def validate_year(value):
    current_year = now().year
    if value < 1950 or value > current_year:
        raise ValidationError(f"Year must be between 1950 and {current_year}.")


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name


class Studio(models.Model):
    name = models.CharField(max_length=100)
    founded_year = models.IntegerField(validators=[validate_year])
    description = models.TextField()
    country = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Game(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    release_year = models.IntegerField(validators=[validate_year])
    genre = models.ManyToManyField(Genre)
    studio = models.ForeignKey(Studio, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    favorite_games = models.ManyToManyField(Game, blank=True, related_name="favorited_by")


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments")
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField()
    post_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.post_date}: {self.text[:50]}"
