from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from accounts.models import Profile
from accounts.utils import async_send_mail
from .forms import AccountInfoForm, CustomUserCreationForm, PasswordChangeForm, ReviewForm, SocialAccountsForm, UserInfoForm, UserProfileUpdateForm
from django.http import JsonResponse
from django.utils.timezone import now
from django_otp.plugins.otp_email.models import EmailDevice  # type: ignore
from django.conf import settings
from django_otp.plugins.otp_totp.models import TOTPDevice  # type: ignore
from django.contrib.auth.decorators import login_required
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator


def register_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(request=request)
            login(request, user)
            async_send_mail(
                "Welcome to Our Service",
                f"Thank you for registering!\nFor security, we recommend enabling 2FA.\nFrom Device: {request.META['HTTP_USER_AGENT']} | IP: {request.META['REMOTE_ADDR']}",
                settings.DEFAULT_FROM_EMAIL,
                user.email,
            )
            return redirect("dashboard")
    else:
        form = CustomUserCreationForm()
    return render(request, "auth/register.html", {"form": form})


def login_view(request):  # sourcery skip: low-code-quality
    if request.user.is_authenticated:
        return redirect("dashboard")
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            return _login_view(form, request)
    else:
        form = AuthenticationForm()

    return render(request, "auth/login.html", {"form": form})


def _login_view(form, request):
    user = form.get_user()
    has_totp = TOTPDevice.objects.filter(
        user=user, confirmed=True).exists()
    has_email_otp = EmailDevice.objects.filter(
        user=user, confirmed=True).exists()

    if not user.has_active_session():
        user.set_session_expiration()

    login(request, user)
    profile = Profile.objects.filter(user=user).first()
    async_send_mail(
        "Login Notification",
        f"You have logged in successfully.\n\nIf this wasn't you, please contact support.\nFor security, we recommend enabling 2FA.\nFrom Device: {request.META.get('HTTP_USER_AGENT', 'Unknown')} | IP: {request.META.get('REMOTE_ADDR', 'Unknown')}",
        settings.DEFAULT_FROM_EMAIL,
        user.email,
    )

    if has_email_otp:
        device = EmailDevice.objects.filter(
            user=user, confirmed=True).first()
        if device:
            code = device.generate_challenge()
            async_send_mail(
                "Your OTP Code",
                f"Your OTP code is: {code}",
                settings.DEFAULT_FROM_EMAIL,
                user.email,
            )
            messages.info(
                request, "An OTP has been sent to your email.")
            return redirect("verify_email_otp")

    if user.is_staff and not has_totp and not has_email_otp:
        return redirect("/admin")
    if has_totp:
        return redirect("verify_email_otp")
    return redirect("dashboard")


@login_required
def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
def admin_view(request):
    return redirect("/admin")


@login_required
def session_status(request):
    if request.user.is_authenticated:
        expired = request.user.session_expires_at and request.user.session_expires_at <= now()
        return JsonResponse({"expired": expired})
    return JsonResponse({"expired": True})


@login_required
def payment_required(request):
    return render(request, "payments/initiate_payment.html")


@login_required
def profile_settings(request):
    user = request.user
    has_totp = TOTPDevice.objects.filter(user=user, confirmed=True).exists()
    has_email_otp = EmailDevice.objects.filter(
        user=user, confirmed=True).exists()
    if request.method == "POST":
        form = UserProfileUpdateForm(
            request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("profile_settings")
        else:
            print(form.errors)
            messages.error(request, "There was an error updating your profile.")
    else:
        form = UserProfileUpdateForm(instance=user)

    context = {
        "totp_enabled": has_totp,
        "email_otp_enabled": has_email_otp,
    }

    return render(request, "auth/profile.html", {"form": form, 'context': context})


def save_profile_step(profile, cleaned_data, step):
    fields_map = {
        1: ["nickname", "first_name", "last_name"],
        2: ["phone_number", "address", "date_of_birth"],
        3: ["profile_picture", "bio"],
        4: ["nickname", "first_name", "last_name", "phone_number", "address", "date_of_birth", "profile_picture", "bio"],
    }
    for field in fields_map.get(step, []):
        setattr(profile, field, cleaned_data.get(field))
    profile.save()


@login_required
def profile_onboarding(request):  # sourcery skip: low-code-quality
    user = request.user
    profile, _ = Profile.objects.get_or_create(user=user)

    steps = {
        1: "User Info",
        2: "Account Info",
        3: "Social Accounts",
        4: "Review",
        5: "Complete",
    }
    current_step = request.session.get("onboarding_step", 1)
    current_step = max(1, min(current_step, len(steps)))
    progress = (current_step / len(steps)) * 100
    form_classes = {
        1: UserInfoForm,
        2: AccountInfoForm,
        3: SocialAccountsForm,
        4: ReviewForm,
        5: None,
    }
    form_class = form_classes.get(current_step)
    if request.method == "POST":
        form = form_class(request.POST, request.FILES, instance=profile) if form_class else None
    else:
        form = form_class(instance=profile) if form_class else None
    if request.method == "POST":
        if "previous" in request.POST:
            current_step = max(1, current_step - 1)
            request.session["onboarding_step"] = current_step
            return redirect("profile_onboarding")

        if form is None or form.is_valid():
            if form:
                profile = form.save(commit=False)

                if current_step == 4:
                    for field, value in form.cleaned_data.items():
                        if value not in [None, '', [], {}]:
                            setattr(profile, field, value)
                else:
                    save_profile_step(profile, form.cleaned_data, current_step)
                profile.save()
            if "next" in request.POST:
                if current_step < len(steps):
                    current_step += 1
                    request.session["onboarding_step"] = current_step
                    return redirect("profile_onboarding")
                else:
                    request.session.pop("onboarding_step", None)
                    return redirect("dashboard")
    return render(request, "auth/onboarding/onboarding_base.html", {
        "steps": steps,
        "current_step": current_step,
        "form": form,
        "progress": progress,
    })


@login_required
def enable_email_otp(request):
    if request.method == "POST":
        email_otp_enabled = request.POST.get("email_otp") == "on"

        device, created = EmailDevice.objects.get_or_create(
            user=request.user, name="Device OTP")
        device_otp = TOTPDevice.objects.filter(user=request.user).first()

        if email_otp_enabled:
            if not device.confirmed:
                code = device.generate_challenge()
                async_send_mail(
                    "Your OTP Code",
                    f"Your OTP code is: {code}",
                    settings.DEFAULT_FROM_EMAIL,
                    [request.user.email],
                )
                messages.info(
                    request, "An OTP has been sent to your email for verification.")

                # Disable TOTP if it exists
                if device_otp:
                    device_otp.confirmed = False
                    device_otp.save()

                device.confirmed = True
                device.save()
                messages.success(request, "Email OTP has been enabled.")
                return redirect("verify_email_otp")
        else:
            if device.confirmed:
                device.confirmed = False
                device.save()
                messages.success(request, "Email OTP has been disabled.")
            return redirect("profile_settings")

    return redirect("profile_settings")


@login_required
def disable_2fa(request):
    """Disable both TOTP and Email OTP for the logged-in user."""
    email_device = EmailDevice.objects.filter(user=request.user).first()
    if email_device:
        email_device.confirmed = False
        email_device.save()

    device_otp = TOTPDevice.objects.filter(user=request.user).first()
    if device_otp:
        device_otp.confirmed = False
        device_otp.save()
    messages.success(
        request, "Two-factor authentication (2FA) has been disabled for your account.")

    return redirect("profile_settings")


@login_required
@csrf_protect
def verify_otp(request):
    email_device = EmailDevice.objects.filter(
        user=request.user, confirmed=True).first()
    device_otp = TOTPDevice.objects.filter(
        user=request.user, confirmed=True).first()
    template = None
    if email_device is not None:
        template = "auth/verify_email_otp.html"
    elif device_otp is not None:
        template = "auth/verify_totp_otp.html"
    if request.method == "POST":
        token = request.POST.get("token", "").strip()
        token = int(token) if token.isdigit() else token
        profile = Profile.objects.filter(user=request.user).first()
        nickname = profile.nickname if profile else None
        first_name = profile.first_name if profile else None
        last_name = profile.last_name if profile else None
        success_message = None
        try:
            if token and email_device and email_device.verify_token(str(token)):
                email_device.confirmed = True
                email_device.save()
                success_message = "Email OTP has been verified."
            elif token and device_otp and device_otp.verify_token(str(token)):
                device_otp.confirmed = True
                device_otp.save()
                success_message = "TOTP has been verified."
            else:
                messages.error(request, "Invalid OTP. Try again.")
                return render(request, template, {"totp_enabled": device_otp})
        except Exception:
            messages.error(request, "Invalid OTP. Please try again.")
            return render(request, template, {"totp_enabled": device_otp})
        messages.success(request, success_message)
        if not (nickname and first_name and last_name):
            return redirect("profile_settings")
        elif request.user.is_staff:
            return redirect("/admin")
        else:
            return redirect("dashboard")

    return render(request, template, {"totp_enabled": device_otp is not None})


@login_required
def resend_verification_email(request):
    email_device = EmailDevice.objects.filter(
        user=request.user, confirmed=True).first()
    if email_device:
        code = email_device.generate_challenge()
        async_send_mail(
            "Your OTP Code",
            f"Your OTP code is: {code}",
            settings.DEFAULT_FROM_EMAIL,
            request.user.email,
        )
        messages.info(request, "An OTP has been sent to your email.")
        return JsonResponse({"success": True, "message": "OTP sent successfully."})
    return JsonResponse({"success": False, "message": "Could not resend OTP."}, status=400)


@login_required
def enforce_admin_2fa(request):
    """Check if admin user has 2FA enabled, if not redirect to 2FA setup."""
    if request.user.is_staff:
        has_totp = TOTPDevice.objects.filter(
            user=request.user, confirmed=True).exists()
        has_email_otp = EmailDevice.objects.filter(
            user=request.user, confirmed=True).exists()

        if not (has_totp or has_email_otp):
            return redirect("2fa_setup")

    return redirect("/admin")

# Password Reset Request


def request_password_reset(request):
    if request.method == "POST":
        email = request.POST.get("email")
        user = get_object_or_404(request.user, email=email)

        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        reset_url = f"https://{settings.ALLOWED_HOSTS}/reset-password/{uid}/{token}/"
        async_send_mail(
            "Password Reset Request",
            f"Click the link to reset your password: {reset_url}",
            settings.DEFAULT_FROM_EMAIL,
            user.email,
        )
        return redirect("password_reset_done")

    return render(request, "auth/password_reset.html")

# Password Reset Confirm


def reset_password(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = request.user.objects.get(pk=uid)

        if request.method == "POST":
            new_password = request.POST.get("password")
            user.set_password(new_password)
            user.save()
            return redirect("login")

        return render(request, "auth/password_reset_confirm.html", {"valid": True})
    except Exception:
        return render(request, "auth/password_reset_confirm.html", {"valid": False})

# Change Password (For logged-in users)


@login_required
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return redirect("profile_settings")
    else:
        form = PasswordChangeForm(request.user)
    return render(request, "auth/change_password.html", {"form": form})
