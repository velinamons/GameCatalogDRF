from django.urls import reverse
from rest_framework.test import APIClient
import pytest

pytestmark = pytest.mark.django_db


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def paths(game, genre):
    return {
        "genre_list": reverse("genre-list"),
        "game_detail": reverse("game-detail", kwargs={"pk": game.id}),
        "toggle_favorite": reverse("game-toggle-favorite", kwargs={"pk": game.id}),
    }


def test_genre_list(api_client, genre, paths):
    response = api_client.get(paths["genre_list"])
    assert response.status_code == 200
    assert response.json() == [
        {"id": genre.id, "name": genre.name, "description": genre.description}
    ]


def test_game_detail(api_client, game, paths):
    response = api_client.get(paths["game_detail"])
    assert response.status_code == 200
    assert response.json()["name"] == game.name


def test_add_to_favorites(api_client, user, game, paths, access_token):
    token = access_token(user)

    response = api_client.post(
        paths["toggle_favorite"], HTTP_AUTHORIZATION=f"Bearer {token}"
    )

    assert response.status_code == 200
    assert response.json()["is_favorite"] is True
    assert game in user.favorite_games.all()


def test_remove_from_favorites(api_client, user, game, paths, access_token):
    user.favorite_games.add(game)

    token = access_token(user)

    response = api_client.post(
        paths["toggle_favorite"], HTTP_AUTHORIZATION=f"Bearer {token}"
    )

    assert response.status_code == 200
    assert response.json()["is_favorite"] is False
    assert game not in user.favorite_games.all()


def test_toggle_favorite_unauthorized(api_client, paths):
    response = api_client.post(paths["toggle_favorite"])

    assert response.status_code == 401
    assert response.json()["detail"] == "Authentication credentials were not provided."


def test_toggle_favorite_invalid_token(api_client, paths):
    response = api_client.post(
        paths["toggle_favorite"], HTTP_AUTHORIZATION="Bearer invalid_token"
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Given token not valid for any token type"
