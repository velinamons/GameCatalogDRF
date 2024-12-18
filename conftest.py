import pytest
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken

from game_catalog.models import Game, Genre, Studio

User = get_user_model()


@pytest.fixture
def user():
    return User.objects.create_user(username="testuser123", password="password123")


@pytest.fixture
def admin_user():
    return User.objects.create_superuser(username="testadmin123", password="admin123")


@pytest.fixture
def access_token(user):
    """
    Fixture to generate a JWT access token for a given user.
    """
    def _get_access_token(user_instance=None):
        user_instance = user_instance or user
        token = AccessToken.for_user(user_instance)
        return str(token)

    return _get_access_token


@pytest.fixture
def genre():
    return Genre.objects.create(name="Action", description="Action games")


@pytest.fixture
def studio():
    return Studio.objects.create(
        name="Epic Games",
        founded_date="1991-01-01",
        description="Game studio",
        country="USA",
    )


@pytest.fixture
def game(genre, studio):
    game = Game.objects.create(
        name="Fortnite",
        description="Battle Royale game",
        release_date="2017-07-25",
        studio=studio,
    )
    game.genre.add(genre)
    return game
