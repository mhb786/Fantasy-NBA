from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from mysite.models import Profile

class Command(BaseCommand):
    help = 'Creates profiles for existing users'

    def handle(self, *args, **options):
        existing_users = User.objects.all()
        for user in existing_users:
            Profile.objects.get_or_create(user=user)
        self.stdout.write(self.style.SUCCESS('Profiles created successfully for existing users'))
