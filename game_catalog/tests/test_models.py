import pytest

from game_catalog.models import Comment

pytestmark = pytest.mark.django_db


def test_genre_str(genre):
    assert str(genre) == "Action"


def test_studio_str(studio):
    assert str(studio) == "Epic Games"


def test_game_str(game):
    assert str(game) == "Fortnite"


def test_user_is_favorite(user, game):
    user.favorite_games.add(game)
    assert user.is_favorite(game) is True


def test_comment_creation(user, game):
    comment = Comment.objects.create(user=user, game=game, text="Great game!")
    assert str(comment).startswith(f"Comment by {user.username}")
