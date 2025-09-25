from django.core.management.base import BaseCommand
from ...factories import CategoryFactory

class Command(BaseCommand):
    help = "Seed the app database with fake categories"

    def add_arguments(self, parser):
        parser.add_argument('--count',
                            type=int, 
                            default=5,
                            choices=(1, 501))

    def handle(self, *args, **options):
        count = options['count']
        CategoryFactory.create_batch(count)
        self.stdout.write(self.style.SUCCESS(f"Created {count} users"))