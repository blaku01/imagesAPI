import os

# set up Django environment
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()
from django.core.management import call_command
from users.tests.factories import AccountTierFactory, ImagesUserFactory

NUM_USERS = 10

# call Django management commands to reset database and run migrations
call_command("reset_db", "--noinput", "--close-sessions")
call_command("migrate")

# create account tiers
basic_tier = AccountTierFactory(
    name="Basic",
    thumbnail_sizes=[200],
    original_file_link=False,
    expiring_link_enabled=False,
)

premium_tier = AccountTierFactory(
    name="Premium",
    thumbnail_sizes=[200, 400],
    original_file_link=True,
    expiring_link_enabled=False,
)

enterprise_tier = AccountTierFactory(
    name="Enterprise",
    thumbnail_sizes=[200, 400],
    original_file_link=True,
    expiring_link_enabled=True,
)

# create users

staff_user = ImagesUserFactory(
    email="admin@admin.com",
    account_tier=enterprise_tier,
    is_staff=True,
    is_superuser=True,
    password="admin",
)

for i in range(NUM_USERS):
    ImagesUserFactory()
