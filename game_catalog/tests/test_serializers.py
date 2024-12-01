import pytest
from django.test import TestCase

from game_catalog.serializers import GameSerializer, RegisterSerializer

pytestmark = pytest.mark.django_db


def test_game_serializer_output(game):
    serializer = GameSerializer(game)
    expected = {
        "id": game.id,
        "name": game.name,
        "description": game.description,
        "release_date": game.release_date,
        "genre": [
            {"id": g.id, "name": g.name, "description": g.description}
            for g in game.genre.all()
        ],
        "studio": {
            "id": game.studio.id,
            "name": game.studio.name,
            "founded_date": game.studio.founded_date,
            "description": game.studio.description,
            "country": game.studio.country,
        },
        "in_favorites": game.favorited_by.count(),
    }

    assert serializer.data == expected


class RegisterSerializerTestCase(TestCase):
    def test_register_serializer_valid(self):
        """Test valid data for RegisterSerializer"""
        data = {
            "username": "testuser123",
            "first_name": "",
            "last_name": "",
            "email": "",
            "password": "password123",
        }

        serializer = RegisterSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data["username"], "testuser123")
        self.assertEqual(serializer.validated_data["password"], "password123")

    def test_register_serializer_invalid_password(self):
        """Test invalid data for password"""
        data = {
            "username": "testuser123",
            "first_name": "",
            "last_name": "",
            "email": "",
            "password": "short",
        }

        serializer = RegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("password", serializer.errors)
        self.assertEqual(
            serializer.errors["password"],
            ["Ensure this field has at least 8 characters."],
        )

    def test_register_serializer_missing_username(self):
        """Test missing username"""
        data = {
            "first_name": "",
            "last_name": "",
            "email": "",
            "password": "password123",
        }

        serializer = RegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("username", serializer.errors)
