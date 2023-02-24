import factory
from django.utils import timezone
from .models import AccountTier


class AccountTierFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AccountTier

    name = factory.Faker('name')
    thumbnail_sizes = [200,]
    original_file_link = True
    expiring_link_enabled = False
    created_at = factory.LazyFunction(timezone.now)