from base_command_class import BaseSeedCommand
from ...factories import ProductFactory

class Command(BaseSeedCommand):
    help = "Seed Product objects"
    factory_class = ProductFactory