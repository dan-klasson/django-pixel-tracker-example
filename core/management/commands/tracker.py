from django.core.management.base import BaseCommand, CommandError
from core.services import TrackerCommand


class Command(BaseCommand):
    help = 'Displays pixel tracking results'

    def add_arguments(self, parser):
        parser.add_argument('--date_from', help='From date')
        parser.add_argument('--date_to', help='To date')

    def handle(self, *args, **options):
        try:
            results = TrackerCommand.execute({
                'date_from': options.get('date_from'),
                'date_to': options.get('date_to')
            })
        except CommandError as e:
            return self.stdout.write(str(e))

        if len(results) == 0:
            return self.stdout.write('No records found')

        self.stdout.write('| url\t\t\t| page views \t| visitors')

        for result in results:
            self.stdout.write(
                f"| {result.get('url')}\t\t| {result.get('page_views')}\t\t| {result.get('visitors')}")
