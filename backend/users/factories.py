import factory
from django.contrib.auth import get_user_model
from django.utils import timezone

from .models import AccountTier

User = get_user_model()


class AccountTierFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AccountTier

    name = factory.Faker("name")
    thumbnail_sizes = [
        200,
    ]
    original_file_link = True
    expiring_link_enabled = False
    created_at = factory.LazyFunction(timezone.now)


class CustomUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Sequence(lambda n: f"user{n}@example.com")
    account_tier = factory.SubFactory(AccountTierFactory)
    password = factory.PostGenerationMethodCall("set_password", "password")
