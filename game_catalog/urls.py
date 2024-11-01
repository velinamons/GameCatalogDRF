from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GameViewSet, GenreViewSet, StudioViewSet

router = DefaultRouter()
router.register(r'games', GameViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'studios', StudioViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
