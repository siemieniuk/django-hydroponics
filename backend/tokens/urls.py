from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from tokens.views import user_registration_view

urlpatterns = [
    path(
        "obtain",
        TokenObtainPairView.as_view(),
        name="token_obtain",
    ),
    path(
        "refresh",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),
    path("register", user_registration_view, name="user_register"),
]
