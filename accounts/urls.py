from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import UserRegisterView, VerifyEmailView, UserProfileRetrieveUpdateView

app_name = "accounts"
urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="register"),
    path(
        "verify-email/<uidb64>/<token>/", VerifyEmailView.as_view(), name="verify_email"
    ),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("profile/", UserProfileRetrieveUpdateView.as_view(), name="profile"),
]
