from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from game_catalog.views import RegisterView

urlpatterns = [
    path('', RedirectView.as_view(url='/register/', permanent=False)),
    path("register/", RegisterView.as_view(), name="register"),
    path('admin/', admin.site.urls),
    path('api/', include('game_catalog.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
