from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Create a demo user for testing'

    def handle(self, *args, **options):
        username = 'demo'
        email = 'demo@example.com'
        password = 'demo123'

        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(f'User {username} already exists')
            )
        else:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            self.stdout.write(
                self.style.SUCCESS(f'Created demo user: {username} (password: {password})')
            )

