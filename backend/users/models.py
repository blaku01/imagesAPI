from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils import timezone

# Create your models here.


class AccountTier(models.Model):
    name = models.CharField(max_length=255)
    thumbnail_sizes = ArrayField(
        models.IntegerField()
    )  # using ManyToMany field could also be an option.
    original_file_link = models.BooleanField(default=False)
    expiring_link_enabled = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        account_tier, _ = AccountTier.objects.get_or_create(
            name="Enterprise",
            thumbnail_sizes=[200, 400],
            original_file_link=True,
            expiring_link_enabled=True,
        )
        extra_fields["account_tier_id"] = account_tier.id
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    account_tier = models.ForeignKey(
        AccountTier, to_field="name", default="Basic", on_delete=models.PROTECT
    )
    objects = CustomUserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email
