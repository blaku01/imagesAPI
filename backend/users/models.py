from django.db import models
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField

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