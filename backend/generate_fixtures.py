import getopt
import os
import sys

# set up Django environment
import django

argumentList = sys.argv[1:]
options = "c:m:e:p:"  # do not use these.
long_options = ["clear_db", "migrate", "admin_email", "admin_password"]
arguments, values = getopt.getopt(argumentList, options, long_options)

short_to_long = {
    "c": "clear_db",
    "m": "migrate",
    "e": "admin_email",
    "p": "admin_password",
}
config = {
    "admin_email": "admin@admin.com",
    "admin_password": "admin",
    "migrate": "True",
    "clear_db": "True",
}

for current_argument, current_value in arguments:
    if len(current_argument) == 2:
        current_argument = short_to_long[current_argument[1:]]
    config[current_argument] = current_value

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()
from django.core.management import call_command
from users.tests.factories import AccountTierFactory, ImagesUserFactory

# call Django management commands to reset database and run migrations
if config["clear_db"] == "True":
    call_command("reset_db", "--noinput", "--close-sessions")
if config["migrate"] == "True":
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
        email=config["admin_email"],
        account_tier=enterprise_tier,
        is_staff=True,
        is_superuser=True,
        password=config["admin_password"],
    )
