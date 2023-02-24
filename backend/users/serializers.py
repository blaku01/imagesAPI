from rest_framework import serializers
from .models import AccountTier

class AccountTierSerializer(serializers.ModelSerializer):
    thumbnail_sizes = serializers.ListField(child=serializers.IntegerField())
    class Meta:
        model = AccountTier
        fields = ('id', 'name', 'thumbnail_sizes', 'original_file_link', 'expiring_link_enabled', 'created_at')