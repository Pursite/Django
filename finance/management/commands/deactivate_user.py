from shlex import join
from django.core.management import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    
    def add_arguments(self, parser):
        parser.add_argument("username", nargs="+", type=str)
        parser.add_argument(
            "--isstaff", help="deactive if use is not staff"
        )


    def handle(self, *args, **options):
        usernames = options['username']
        users = User.objects.filter(username__in=usernames)

        if options['isstaff']:
            users.filter(is_staff=False)

        if users.exists():
            users.update(is_active=True)


        print(", ".join(users.values_list('username', flat=True)))