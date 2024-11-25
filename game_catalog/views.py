from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response

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
    queryset = Game.objects.select_related("studio").prefetch_related("genre")
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return GameWriteSerializer
        return GameSerializer

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


class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommentDetailView(generics.RetrieveDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsOwnerOrAdmin()]


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
