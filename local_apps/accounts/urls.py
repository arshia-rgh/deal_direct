from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from local_apps.accounts.views.auth_views import (
    UserRegisterView,
    VerifyEmailView,
    UserProfileRetrieveUpdateView,
    UserPasswordChangeView,
    PasswordResetRequestAPIView,
    PasswordResetConfirmAPIView,
)
from local_apps.accounts.views.payment_views import (
    IncreaseWalletAPIView,
    VerifyDepositAPIView,
)
from local_apps.accounts.views.session_auth_views import (
    SessionListAPIView,
    SessionLogoutDestroyView,
)

app_name = "accounts"
urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="register"),
    path(
        "verify-email/<str:uidb64>/<str:token>/",
        VerifyEmailView.as_view(),
        name="verify_email",
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
    path(
        "reset-password/<str:uidb64>/<str:token>/",
        PasswordResetConfirmAPIView.as_view(),
        name="password_reset_confirm",
    ),
    # sessions
    path("sessions/", SessionListAPIView.as_view(), name="session_list"),
    path(
        "sessions/<str:session_key>/logout/",
        SessionLogoutDestroyView.as_view(),
        name="session_logout",
    ),
    # payments
    path("deposit/", IncreaseWalletAPIView.as_view(), name="deposit"),
    path("deposit/verify/", VerifyDepositAPIView.as_view(), name="verify-deposit"),
]
