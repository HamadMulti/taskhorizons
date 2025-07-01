from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

class Command(BaseCommand):
    help = "Creates a default admin user if none exists"

    def handle(self, *args, **kwargs):
        User = get_user_model()

        admin_email = os.getenv("ADMIN_EMAIL", "taskhorizonapp@gmail.com")
        admin_username = os.getenv("ADMIN_USERNAME", "hamad")
        admin_password = os.getenv("ADMIN_PASSWORD", "hamad@123@")

        if not User.objects.filter(is_superuser=True).exists():
            User.objects.create_superuser(
                username=admin_username,
                email=admin_email,
                password=admin_password
            )
            self.stdout.write(self.style.SUCCESS(f"Superuser '{admin_username}' created successfully."))
        else:
            self.stdout.write(self.style.WARNING("Superuser already exists. No action taken."))
