from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name


class Studio(models.Model):
    name = models.CharField(max_length=100)
    founded_date = models.DateField()
    description = models.TextField()
    country = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Game(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    release_date = models.DateField()
    genre = models.ManyToManyField(Genre)
    studio = models.ForeignKey(Studio, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    favorite_games = models.ManyToManyField(
        Game, blank=True, related_name="favorited_by"
    )

    def is_favorite(self, game):
        return self.favorite_games.filter(pk=game.pk).exists()


class Comment(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments"
    )
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField()
    post_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.post_date}: {self.text[:50]}"
