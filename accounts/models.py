from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.timezone import now, timedelta
from django.db.models.signals import post_save
from django.dispatch import receiver


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)



class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    session_expires_at = models.DateTimeField(null=True, blank=True)
    last_seen = models.DateTimeField(null=True, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def set_session_expiration(self, duration_hours=12):
        """Sets session expiration timestamp"""
        self.session_expires_at = now() + timedelta(hours=duration_hours)
        self.save()
        
    def has_active_session(self):
        """Check if the user's session is still valid"""
        return self.session_expires_at and self.session_expires_at > now()
    
    def update_last_seen(self):
        self.last_seen = now()
        self.save()

class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="profile")
    nickname = models.CharField(max_length=30, blank=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    phone_number = models.CharField(max_length=20, unique=True, blank=True, null=True, default=None)
    address = models.CharField(max_length=255, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to="profile_pictures/", blank=True, null=True)
    bio = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user_type = models.CharField(max_length=20, choices=[
        ('free', 'Free'),
        ('day', 'Day'),
        ('week', 'Week'),
        ('month', 'Month'),
        ('half_year', 'Half Year'),
        ('year', 'Year'),
    ], default='free')
    is_premium = models.BooleanField(default=False)
    premium_expiry = models.DateTimeField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    is_suspended = models.BooleanField(default=False)
    is_banned = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    free_access_start = models.DateTimeField(null=True, blank=True)

    def has_valid_free_access(self):
        """Return True if user has valid free 3-hour access."""
        if self.free_access_start and not self.is_premium and not self.user.is_staff:
            expiry_time = self.free_access_start + timedelta(hours=3)
            return now() < expiry_time
        return False


    def __str__(self):
        return f"Profile of {self.user.email}"


@receiver(post_save, sender=CustomUser)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=CustomUser)
def save_profile(sender, instance, **kwargs):
    """Ensure the profile exists before saving"""
    if hasattr(instance, "profile"):
        instance.profile.save()
