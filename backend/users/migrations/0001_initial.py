# Generated by Django 4.1.7 on 2023-02-24 16:10

import django.contrib.postgres.fields
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AccountTier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('thumbnail_sizes', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), size=None)),
                ('original_file_link', models.BooleanField(default=False)),
                ('expiring_link_enabled', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
