"""Management command to create a superuser if it does not already exist."""

import os
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Custom Django management command to create a superuser automatically."""

    help = "Create a superuser if one does not exist"

    def handle(self, *args, **options):
        """
        Entry point for the command execution.

        Reads superuser credentials from environment variables and creates
        a superuser if one does not already exist.
        """
        User = get_user_model()

        username = os.getenv("DJANGO_SUPERUSER_USERNAME")
        email = os.getenv("DJANGO_SUPERUSER_EMAIL")
        password = os.getenv("DJANGO_SUPERUSER_PASSWORD")

        if not username or not email or not password:
            self.stdout.write(self.style.ERROR("Superuser credentials not provided in env variables."))
            return

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f"Superuser '{username}' created."))
        else:
            self.stdout.write(self.style.SUCCESS(f"Superuser '{username}' already exists."))
