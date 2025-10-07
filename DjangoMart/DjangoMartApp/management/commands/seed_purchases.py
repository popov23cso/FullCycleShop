from .base_command_class import BaseSeedCommand
from ...factories import PurchaseFactory

class Command(BaseSeedCommand):
    help = "Seed Purchase objects"
    factory_class = PurchaseFactory