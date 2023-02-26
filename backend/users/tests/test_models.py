from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from users.factories import AccountTierFactory

User = get_user_model()


class AccountTierModelTest(TestCase):
    def test_str_representation(self):
        tier = AccountTierFactory(name="Basic")
        self.assertEqual(str(tier), "Basic")


class ImagesUserModelTest(TestCase):
    def test_create_user_without_email(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(email="", password="password")

    def test_create_user_with_email(self):
        account_tier = AccountTierFactory(
            name="Enterprise",
            thumbnail_sizes=[200, 400],
            original_file_link=True,
            expiring_link_enabled=True,
        )
        user = get_user_model().objects.create_user(
            email="user@example.com", password="password", account_tier=account_tier
        )
        self.assertEqual(user.email, "user@example.com")
        self.assertTrue(user.check_password("password"))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser_with_email(self):
        account_tier = AccountTierFactory(
            name="Enterprise",
            thumbnail_sizes=[200, 400],
            original_file_link=True,
            expiring_link_enabled=True,
        )
        superuser = get_user_model().objects.create_superuser(
            email="superuser@example.com",
            password="password",
            account_tier=account_tier,
        )
        self.assertEqual(superuser.email, "superuser@example.com")
        self.assertEqual(str(superuser), "superuser@example.com")
        self.assertTrue(superuser.check_password("password"))
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
        self.assertEqual(superuser.account_tier.name, "Enterprise")
        self.assertEqual(list(superuser.account_tier.thumbnail_sizes), [200, 400])
        self.assertTrue(superuser.account_tier.original_file_link)
        self.assertTrue(superuser.account_tier.expiring_link_enabled)
        self.assertLess(
            (timezone.now() - superuser.account_tier.created_at).total_seconds(), 1
        )
