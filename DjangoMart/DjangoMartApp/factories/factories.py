import factory
from faker import Faker
from django.contrib.auth.hashers import make_password
from ..models import (User, Brand, Category,
                     Product, Purchase, PurchaseItem,
                     Review)
from datetime import datetime, timezone
from django.utils.text import slugify
from .utility import get_weighted_date

fake = Faker()

class BaseFactory(factory.django.DjangoModelFactory):
    class Meta:
        abstract = True

    # define the common columns that are present accross all models
    generated_date = factory.LazyFunction(lambda: get_weighted_date())

    is_auto_generated = True

class UserFactory(BaseFactory):
    class Meta:
        model = User

    username = factory.Faker('user_name')
    email = factory.Faker('email')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    available_tokens = factory.Faker('pyint', min_value=0, max_value=20000)
    password = factory.LazyFunction(lambda: make_password('defaultpassword123'))


class BrandFactory(BaseFactory):
    class Meta:
        model = Brand

    title = factory.Faker('catch_phrase')
    description = factory.Faker('word')

class CategoryFactory(BaseFactory):
    class Meta:
        model = Category

    title = factory.Faker('catch_phrase')

    # turn title with spaces into valid slugs - Car Parts => car-parts
    slug = factory.LazyAttribute(lambda obj: slugify(obj.title))
    description = factory.Faker('word')
    is_main_category = True 
    is_active = True

class ProductFactory(BaseFactory):
    class Meta:
        model = Product

    title = factory.Faker('catch_phrase')
    description = factory.Faker('word')
    price = factory.Faker('pyint', min_value=250, max_value=4500)
    brand = factory.Iterator(Brand.objects.all())
    stock = factory.Faker('pyint', min_value=0, max_value=250)
    rating = factory.Faker('pyfloat', min_value=0.0, max_value=5.0, right_digits=2)
    rating_count = factory.Faker('pyint', min_value=0, max_value=900)
    sales_count = factory.Faker('pyint', min_value=0, max_value=1000)
    category = factory.Iterator(Category.objects.all())

class PurchaseFactory(BaseFactory):
    class Meta:
        model = Purchase

    user = factory.Iterator(User.objects.all())
    total_price = factory.Faker('pyint', min_value=250, max_value=9000)


class PurchaseItemFactory(BaseFactory):
    class Meta:
        model = PurchaseItem

    product = factory.Iterator(Product.objects.all())
    product_name = factory.LazyAttribute(lambda obj: obj.product.title)
    quantity = factory.Faker('pyint', min_value=1, max_value=5)
    price_at_purchase = factory.LazyAttribute(lambda obj: obj.quantity * obj.product.price)
    purchase = factory.SubFactory(PurchaseFactory)

    @factory.post_generation
    def set_purchase_total(obj, create, extracted, **kwargs):
        # override total generated in purchase
        obj.purchase.total_price = obj.price_at_purchase
        obj.purchase.save()

class ReviewFactory(BaseFactory):
    class Meta:
        model = Review
    user = factory.Iterator(User.objects.all())
    purchase_item = factory.SubFactory(PurchaseItemFactory)
    product = factory.LazyAttribute(lambda obj: obj.purchase_item.product)
    rating = factory.Faker('pyint', min_value=1, max_value=5)
    comment = factory.Faker('sentence')
    
