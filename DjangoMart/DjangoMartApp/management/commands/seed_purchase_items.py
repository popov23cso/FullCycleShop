from base_command_class import BaseSeedCommand
from ...factories import PurchaseItemFactory

class Command(BaseSeedCommand):
    help = "Seed PurchaseItem objects"
    factory_class = PurchaseItemFactory