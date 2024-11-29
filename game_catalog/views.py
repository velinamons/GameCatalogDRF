from rest_framework import generics, status, viewsets 
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse

from . import actions
from .custom_permissions import (
    IsAdminOrReadOnly,
    IsOwnerOrAdmin,
)

from .models import Comment, CustomUser, Game, Genre, Studio
from .serializers import (
    CommentSerializer,
    GenreSerializer,
    GameSerializer,
    GameWriteSerializer,
    StudioSerializer,
    ToggleFavoriteResponseSerializer,
    UserExtendedInfoSerializer,
    UserShortInfoSerializer,
    RegisterSerializer, ToggleFavoriteResponseSerializer,
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


@extend_schema_view(
    list=extend_schema(
        description="Retrieve a list of all games. Read-only for everyone.",
        responses=GameSerializer,
    ),
    retrieve=extend_schema(
        description="Retrieve details of a specific game. Read-only for everyone.",
        responses=GameSerializer,
    ),
    create=extend_schema(
        description="Create a new game entry. Admins only.",
        request=GameWriteSerializer,
        responses=GameSerializer,
    ),
    update=extend_schema(
        description="Update an existing game entry. Admins only.",
        request=GameWriteSerializer,
        responses=GameSerializer,
    ),
    partial_update=extend_schema(
        description="Partially update a game entry. Admins only.",
        request=GameWriteSerializer,
        responses=GameSerializer,
    ),
    destroy=extend_schema(
        description="Delete a game entry. Admins only.",
        responses=OpenApiResponse(description="No content"),
    ),
)
class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.select_related("studio").prefetch_related("genre")
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return GameWriteSerializer
        return GameSerializer

    @extend_schema(
        description="Toggle a game in or out of the user's favorites list. Requires authentication.",
        request=None,
        responses={
            200: ToggleFavoriteResponseSerializer,
        }
    )
    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def toggle_favorite(self, request, pk=None):
        game = self.get_object()
        user = request.user

        actions.toggle_favorite(user, game)

        response_data = {
            "is_favorite": user.is_favorite(game),
            "user": UserShortInfoSerializer(user).data,
        }

        serializer = ToggleFavoriteResponseSerializer(data=response_data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


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
    queryset = CustomUser.objects.prefetch_related("favorite_games")

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
