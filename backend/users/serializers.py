from rest_framework import serializers

from .models import AccountTier, ImagesUser


class AccountTierSerializer(serializers.ModelSerializer):
    thumbnail_sizes = serializers.ListField(child=serializers.IntegerField())

    class Meta:
        model = AccountTier
        fields = (
            "id",
            "name",
            "thumbnail_sizes",
            "original_file_link",
            "expiring_link_enabled",
            "created_at",
        )


class ImagesUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = ImagesUser
        fields = ("id", "email", "password", "account_tier")
        extra_kwargs = {"password": {"write_only": True}}
