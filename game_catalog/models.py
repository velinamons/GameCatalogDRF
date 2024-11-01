from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class Studio(models.Model):
    name = models.CharField(max_length=100)
    founded_year = models.IntegerField()
    description = models.TextField()
    country = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Game(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    release_year = models.IntegerField()
    genre = models.ManyToManyField(Genre)
    studio = models.ForeignKey(Studio, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
