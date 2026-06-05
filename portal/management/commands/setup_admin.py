from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Creates or updates the admin portal superuser (soorya)'

    def handle(self, *args, **options):
        username = 'soorya'
        password = 'soorya2006'
        email = 'soorya@overclock.local'

        user, created = User.objects.get_or_create(username=username, defaults={'email': email})
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save()

        if created:
            self.stdout.write(self.style.SUCCESS(f'Created admin user: {username}'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Updated admin user: {username}'))

        self.stdout.write(f'  Login at http://127.0.0.1:8000/admin-portal/login/')
        self.stdout.write(f'  Username: {username}')
        self.stdout.write(f'  Password: {password}')
