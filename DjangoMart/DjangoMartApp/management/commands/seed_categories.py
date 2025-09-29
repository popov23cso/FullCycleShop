from .base_command_class import BaseSeedCommand
from ...factories import CategoryFactory

class Command(BaseSeedCommand):
    help = "Seed Category objects"
    factory_class = CategoryFactory