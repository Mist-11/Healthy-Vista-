from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from users.models import User


class Command(BaseCommand):
    help = 'Creates an admin user if it does not exist'

    def handle(self, *args, **options):
        if not User.objects.filter(name='admin').exists():
            User.objects.create(
                name='admin',
                password=make_password('your_secure_password'),
                email='admin@django.com',
                identity='系统管理员',
                sex='M'
            )
            self.stdout.write(self.style.SUCCESS('成功创建管理员账户！'))
