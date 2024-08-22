from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from accounts.views.auth_views import (
    UserRegisterView,
    VerifyEmailView,
    UserProfileRetrieveUpdateView,
    UserPasswordChangeView,
    PasswordResetRequestAPIView,
)
from accounts.views.payment_views import IncreaseWalletAPIView, VerifyDepositAPIView

app_name = "accounts"
urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="register"),
    path(
        "verify-email/<uidb64>/<token>/", VerifyEmailView.as_view(), name="verify_email"
    ),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("profile/", UserProfileRetrieveUpdateView.as_view(), name="profile"),
    path(
        "profile/password-change/",
        UserPasswordChangeView.as_view(),
        name="change_password",
    ),
    path(
        "reset-password/", PasswordResetRequestAPIView.as_view(), name="password_reset"
    ),
    # payments
    path("deposit/", IncreaseWalletAPIView.as_view(), name="deposit"),
    path("deposit/verify/", VerifyDepositAPIView.as_view(), name="verify-deposit"),
]
