from email import message

from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Print a message in console."

    def add_arguments(self, parser):
        parser.add_argument("--message", '-m', type=str, default=None)

    def handle(self, *args, message, **options):
        if message:
            print(message)
        else:
            raise CommandError("No message was provided!")
