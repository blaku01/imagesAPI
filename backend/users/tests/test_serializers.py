from django.test import TestCase
from rest_framework.exceptions import ValidationError
from users.factories import AccountTierFactory
from users.serializers import AccountTierSerializer, ImagesUserSerializer


class AccountTierSerializerTest(TestCase):
    def test_serializer_with_missing_fields(self):
        serializer = AccountTierSerializer(data={})
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_serializer_with_invalid_thumbnail_sizes(self):
        data = {
            "name": "Basic",
            "thumbnail_sizes": ["not", "integers"],
            "original_file_link": True,
            "expiring_link_enabled": False,
        }
        serializer = AccountTierSerializer(data=data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)


class ImagesUserSerializerTest(TestCase):
    def test_serializer_with_missing_fields(self):
        serializer = ImagesUserSerializer(data={})
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_serializer_with_invalid_email(self):
        data = {
            "email": "not_an_email",
            "password": "password",
            "account_tier": AccountTierFactory(),
        }
        serializer = ImagesUserSerializer(data=data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)
