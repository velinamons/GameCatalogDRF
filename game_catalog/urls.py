from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import GenreViewSet, StudioViewSet, GameViewSet, CommentViewSet, UserViewSet

router = DefaultRouter()
router.register("genres", GenreViewSet)
router.register("studios", StudioViewSet)
router.register("games", GameViewSet)
router.register("comments", CommentViewSet)
router.register("users", UserViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
