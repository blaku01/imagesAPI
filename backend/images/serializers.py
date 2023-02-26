from rest_framework import serializers

from .models import Image


class ListImageSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="images-variants", read_only=True
    )

    class Meta:
        model = Image
        fields = ("id", "name", "url", "created_at")
        read_only_fields = ("id", "name", "created_at")


class DetailImageSerializer(serializers.Serializer):
    thumbnail_urls = serializers.DictField(child=serializers.URLField(), required=False)
    original_image = serializers.URLField(required=False)
    expiring_binary_url = serializers.URLField(required=False)


class CreateImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ("id", "name", "file", "created_at")
        read_only_fields = ("id", "created_at")
