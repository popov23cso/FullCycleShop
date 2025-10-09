from django.core.management.base import BaseCommand

class BaseSeedCommand(BaseCommand):
    help = 'Base command for seeding data'

    # define factory class in subclasses
    factory_class = None

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=1,
            choices=(1, 10, 20, 50, 100,
                    200, 500, 1000, 2000,
                    5000, 10000),
            help='Number of objects to create'
        )

    def handle(self, *args, **options):
        if not self.factory_class:
            self.stderr.write(self.style.ERROR('No factory_class defined'))
            return

        count = options['count']
        self.factory_class.create_batch(count)
        self.stdout.write(
            self.style.SUCCESS(f'Created {count} {self.factory_class.__name__} objects')
        )