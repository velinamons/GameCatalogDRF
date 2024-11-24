from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .custom_permissions import (
    IsAdminOrReadOnly,
    IsOwnerOrAdmin,
    IsAuthenticatedOrReadOnly,
)

from .models import Genre, Studio, Game, Comment, CustomUser
from .serializers import (
    GenreSerializer,
    StudioSerializer,
    GameSerializer,
    GameWriteSerializer,
    CommentSerializer,
    UserExtendedInfoSerializer,
    UserShortInfoSerializer,
    RegisterSerializer,
    GameCommentSerializer,
)


class RegisterView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(user.password)
        user.save()
        return user


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnly]


class StudioViewSet(viewsets.ModelViewSet):
    queryset = Studio.objects.all()
    serializer_class = StudioSerializer
    permission_classes = [IsAdminOrReadOnly]


class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            print("self.action in create, update")
            return GameWriteSerializer
        return GameSerializer

    @action(
        detail=True,
        methods=["get", "post"],
        permission_classes=[IsAuthenticatedOrReadOnly],
    )
    def comments(self, request, pk=None):
        game = self.get_object()
        if request.method == "POST":
            serializer = GameCommentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user, game=game)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        comments = game.comments.all()
        serializer = GameCommentSerializer(comments, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def add_to_favorites(self, request, pk=None):
        game = self.get_object()
        user = request.user
        if game in user.favorite_games.all():
            return Response(
                {"detail": "Game is already in favorites."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.favorite_games.add(game)
        return Response(
            {"detail": "Game added to favorites."}, status=status.HTTP_200_OK
        )

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def remove_from_favorites(self, request, pk=None):
        game = self.get_object()
        user = request.user
        if game not in user.favorite_games.all():
            return Response(
                {"detail": "Game is not in favorites."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.favorite_games.remove(game)
        return Response(
            {"detail": "Game removed from favorites."}, status=status.HTTP_200_OK
        )


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()

    def get_permissions(self):
        if self.action in ["me", "list", "retrieve"]:
            return [IsAuthenticated()]
        return [IsAdminUser()]

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return UserExtendedInfoSerializer
        return UserShortInfoSerializer

    @action(detail=False, methods=["get"])
    def me(self, request):
        serializer = UserExtendedInfoSerializer(request.user)
        return Response(serializer.data)
