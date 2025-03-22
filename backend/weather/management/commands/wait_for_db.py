"""Django management command to wait for the database to become available."""

import time

from django.core.management.base import BaseCommand
from django.db import connections
from django.db.utils import OperationalError


class Command(BaseCommand):
    """Custom Django command that waits for the database to be ready."""

    help = "Wait for database to be ready before continuing."

    def handle(self, *args, **options):
        """
        Entry point for the command execution.

        Repeatedly attempts to connect to the database until successful.
        """
        self.stdout.write("Waiting for database...")
        db_conn = None
        while not db_conn:
            try:
                db_conn = connections['default']
                db_conn.cursor()
            except OperationalError:
                self.stdout.write("Database unavailable, waiting 1 second...")
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS("Database is available!"))
