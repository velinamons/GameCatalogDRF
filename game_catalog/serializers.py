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

    def create(self, validated_data):
        user = CustomUser(
            username=validated_data["username"],
            email=validated_data.get("email", ""),
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", "")
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = "__all__"


class StudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Studio
        fields = "__all__"


class GameCommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "user", "text", "post_date"]
        read_only_fields = ["user", "post_date"]


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "game", "user", "text", "post_date"]
        read_only_fields = ["user", "post_date"]


class GameSerializer(serializers.ModelSerializer):
    studio = StudioSerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True, source="comments_set")
    in_favorites = serializers.SerializerMethodField()

    class Meta:
        model = Game
        fields = ["id", "name", "description", "release_year", "genre", "studio", "in_favorites", "comments"]

    def get_in_favorites(self, obj):
        return obj.favorited_by.count()


class GameWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = "__all__"


class UserAdminSerializer(serializers.ModelSerializer):
    favorite_games = GameSerializer(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = ["id", "username", "first_name", "last_name", "email", "is_staff", "favorite_games"]


class UserPublicSerializer(serializers.ModelSerializer):
    favorite_games = GameSerializer(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = ["username", "favorite_games"]
