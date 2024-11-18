from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.timezone import now


def validate_positive_year(value):
    if value < 1950 or value > now().year:
        raise ValidationError("Year must be between 0 and the current year.")


class Genre(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class Studio(models.Model):
    name = models.CharField(max_length=100)
    founded_year = models.IntegerField(validators=[validate_positive_year])
    description = models.TextField()
    country = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Game(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    release_year = models.IntegerField(validators=[validate_positive_year])
    genre = models.ManyToManyField(Genre)
    studio = models.ForeignKey(Studio, on_delete=models.CASCADE)
    comments = models.ManyToManyField('Comment', blank=True, related_name="games")

    def __str__(self):
        return self.name


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField()
    post_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.post_date}"


class Favorite(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="favorites")
    games = models.ManyToManyField(Game, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Favorites"
