from django.urls import path, reverse_lazy
from django.urls import path
from .views import disable_2fa, admin_view, enable_email_otp, enforce_admin_2fa, payment_required, profile_onboarding, register_view, login_view, logout_view, resend_verification_email, session_status, profile_settings, verify_otp
from two_factor.views import SetupView, BackupTokensView # type: ignore
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("ad/", admin_view, name="admins"),
    path("session-status/", session_status, name="session_status"),
    path("payment-required/", payment_required, name="payment_required"),
    path("profile/", profile_settings, name="profile_settings"),
    path("onboarding/", profile_onboarding, name="profile_onboarding"),
    path("setup/", SetupView.as_view(), name="2fa_setup"),
    path("backup_tokens/", BackupTokensView.as_view(), name="2fa_backup_tokens"),
    path("email/", enable_email_otp, name="enable_email_otp"),
    path("otp/verify/", verify_otp, name="verify_email_otp"),
    path("resend-verification/", resend_verification_email, name="resend_verification"),
    path("disable/", disable_2fa, name="disable_2fa"),
    path("admin/2fa-check/", enforce_admin_2fa, name="enforce_admin_2fa"),
    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(
            template_name="auth/password_reset.html",
            success_url=reverse_lazy("password_reset_done"),
        ),
        name="password_reset",
    ),
    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="auth/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="auth/password_reset_confirm.html",
            success_url=reverse_lazy("password_reset_complete"),
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="auth/password_reset_complete.html",
        ),
        name="password_reset_complete",
    ),
    path(
        "password_change/",
        auth_views.PasswordChangeView.as_view(template_name="auth/password_change.html"),
        name="password_change",
    ),
    path(
        "password_change/done/",
        auth_views.PasswordChangeDoneView.as_view(template_name="auth/password_change_done.html"),
        name="password_change_done",
    ),
]
