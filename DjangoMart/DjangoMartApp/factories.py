import factory
from faker import Faker
from django.contrib.auth.hashers import make_password
from .models import (User, Brand, Category,
                     Product)
from datetime import datetime
import random

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

    is_auto_generated = True

class BrandFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Brand

    title = factory.LazyAttribute(lambda _: fake.word().title())
    description = factory.LazyAttribute(lambda _: fake.word())

    # generate random datetimes that are the same for created and updated date (between 2023 and 2025)
    created_date = factory.LazyFunction(
        lambda: fake.date_time_between(start_date=datetime(2023, 1, 1), end_date=datetime(2025, 12, 31))
    )
    updated_date = factory.SelfAttribute("created_date")
    
    is_auto_generated = True

class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    title = factory.LazyAttribute(lambda _: fake.word().title())
    slug = factory.LazyAttribute(lambda obj: obj.title.lower())
    description = factory.LazyAttribute(lambda _: fake.word())
    is_main_category = True 
    is_active = True

    # generate random datetimes that are the same for created and updated date (between 2023 and 2025)
    created_date = factory.LazyFunction(
        lambda: fake.date_time_between(start_date=datetime(2023, 1, 1), end_date=datetime(2025, 12, 31))
    )
    updated_date = factory.SelfAttribute("created_date")
    
    is_auto_generated = True

class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    title = factory.LazyAttribute(lambda _: fake.word().title())
    description = factory.LazyAttribute(lambda _: fake.word())
    price = factory.LazyAttribute(lambda _: fake.random_int(min=250, max=4500))
    brand = factory.LazyFunction(lambda: random.choice(Brand.objects.all()))
    stock = factory.LazyAttribute(lambda _: fake.random_int(min=0, max=250))
    rating = factory.LazyAttribute(lambda _: fake.random_float(min=0.0, max=5.0))
    ratings_count = factory.LazyAttribute(lambda _: fake.random_int(min=0, max=900))
    sales_count = factory.LazyAttribute(lambda _: fake.random_int(min=0, max=1000))
    category = factory.LazyFunction(lambda: random.choice(Category.objects.all()))

    # generate random datetimes that are the same for created and updated date (between 2023 and 2025)
    created_date = factory.LazyFunction(
        lambda: fake.date_time_between(start_date=datetime(2023, 1, 1), end_date=datetime(2025, 12, 31))
    )
    updated_date = factory.SelfAttribute("created_date")
    
    is_auto_generated = True

    
    
    
