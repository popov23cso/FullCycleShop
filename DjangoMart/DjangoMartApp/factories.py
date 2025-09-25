import factory
from faker import Faker
from django.contrib.auth.hashers import make_password
from .models import User
from datetime import datetime

fake = Faker()

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.LazyAttribute(lambda _: fake.user_name())
    email = factory.LazyAttribute(lambda _: fake.email())
    first_name = factory.LazyAttribute(lambda _: fake.first_name())
    last_name = factory.LazyAttribute(lambda _: fake.last_name())
    available_tokens = factory.LazyAttribute(lambda _: fake.random_int(min=0, max=10000))
    password = factory.LazyFunction(lambda: make_password("defaultpassword123"))

    # generate random datetimes that are the same for created and updated date (between 2023 and 2025)
    created_date = factory.LazyFunction(
        lambda: fake.date_time_between(start_date=datetime(2023, 1, 1), end_date=datetime(2025, 12, 31))
    )
    updated_date = factory.SelfAttribute("created_date")


