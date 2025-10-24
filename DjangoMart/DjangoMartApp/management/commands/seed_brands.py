from .base_command_class import BaseSeedCommand
from ...factories.factories import BrandFactory

class Command(BaseSeedCommand):
    help = "Seed Brand objects"
    factory_class = BrandFactory