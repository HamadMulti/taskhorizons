from django.shortcuts import redirect
from django_otp.plugins.otp_totp.models import TOTPDevice  # type: ignore
from django_otp.plugins.otp_email.models import EmailDevice  # type: ignore
from django.utils.timezone import now
from django.contrib.auth import logout
from .models import Profile
from payments.models import PaymentTransactionHistory
from django.utils.timezone import now
from django.contrib.auth.middleware import get_user
from datetime import timedelta
from django.utils import timezone
from django.utils.timezone import now
from django.contrib.auth import logout
from accounts.models import Profile
from payments.models import PaymentTransactionHistory
from django.utils.dateparse import parse_datetime


class SessionExpirationMiddleware:
    """Middleware to auto-logout users when session expires"""

    def __init__(self, get_response):
        self.get_response = get_response


    def __call__(self, request):
        if request.user.is_authenticated:
            session_expiry = request.session.get("session_expires_at")
            if session_expiry and parse_datetime(session_expiry) <= now():
                profile = Profile.objects.filter(user=request.user).first()
                if profile:
                    if profile.is_premium and self.check_payment_expiry(request.user):
                        profile.is_premium = False
                        profile.user_type = "free"
                        profile.premium_expiry = None
                        profile.save()
                if profile and profile.user_type == "free":
                    if not profile.free_access_start:
                        profile.free_access_start = timezone.now()
                        profile.save()
                    request.session['session_expires_at'] = (profile.free_access_start + timedelta(hours=3)).isoformat()

                    if not profile.is_premium and not profile.has_valid_free_access():
                        logout(request)
        return self.get_response(request)


    def check_payment_expiry(self, user):
        """Return True if payment has expired"""
        payment = PaymentTransactionHistory.objects.filter(
            user=user, payment_status="completed"
        ).order_by("-expiry_time").first()

        if not payment or not payment.expiry_time or payment.expiry_time <= now():
            return True
        return False


class LastSeenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        user = get_user(request)
        if user.is_authenticated:
            user.last_seen = now()
            user.save(update_fields=["last_seen"])
        return response


class EnforceAdmin2FAMiddleware:
    """Middleware to enforce 2FA for admin users."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and request.user.is_staff:
            has_totp = TOTPDevice.objects.filter(user=request.user, confirmed=True).exists()
            has_email_otp = EmailDevice.objects.filter(user=request.user, confirmed=True).exists()

            if (
                not has_totp
                and not has_email_otp
                and request.path.startswith("/admin/")
            ):
                return redirect("2fa_setup")

        return self.get_response(request)
