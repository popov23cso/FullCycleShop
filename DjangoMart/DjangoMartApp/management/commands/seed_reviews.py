from .base_command_class import BaseSeedCommand
from ...factories import ReviewFactory

class Command(BaseSeedCommand):
    help = "Seed Review objects"
    factory_class = ReviewFactory