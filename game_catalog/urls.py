from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import GenreViewSet, StudioViewSet, GameViewSet, UserViewSet, CommentListCreateView, CommentDetailView

router = DefaultRouter()
router.register("genres", GenreViewSet)
router.register("studios", StudioViewSet)
router.register("games", GameViewSet)
router.register("users", UserViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("comments/", CommentListCreateView.as_view(), name="comment-list-create"),
    path("comments/<int:pk>/", CommentDetailView.as_view(), name="comment-detail"),
]
