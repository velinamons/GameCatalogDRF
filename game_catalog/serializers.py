from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from .models import Genre, Studio, Game, Comment, CustomUser


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    email = serializers.EmailField(required=False, allow_blank=True, default="")
    first_name = serializers.CharField(required=False, allow_blank=True, default="")
    last_name = serializers.CharField(required=False, allow_blank=True, default="")

    class Meta:
        model = CustomUser
        fields = ["username", "first_name", "last_name", "email", "password"]


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = "__all__"


class StudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Studio
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "game", "user", "text", "post_date"]
        read_only_fields = ["user", "post_date"]


class GameSerializer(serializers.ModelSerializer):
    studio = StudioSerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    in_favorites = serializers.SerializerMethodField()

    class Meta:
        model = Game
        fields = [
            "id",
            "name",
            "description",
            "release_date",
            "genre",
            "studio",
            "in_favorites",
        ]

    @extend_schema_field(serializers.IntegerField)
    def get_in_favorites(self, obj):
        return obj.favorited_by.count()


class GameWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = "__all__"


class UserExtendedInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "is_staff",
            "favorite_games",
        ]


class UserShortInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["username", "favorite_games"]


class ToggleFavoriteResponseSerializer(serializers.Serializer):
    is_favorite = serializers.BooleanField()
    user = UserShortInfoSerializer()
