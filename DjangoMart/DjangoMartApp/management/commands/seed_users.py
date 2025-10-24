from .base_command_class import BaseSeedCommand
from ...factories.factories import UserFactory

class Command(BaseSeedCommand):
    help = "Seed User objects"
    factory_class = UserFactory