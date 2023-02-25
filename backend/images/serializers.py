from django.urls import reverse
from rest_framework import serializers
from .models import Image

class ListImageSerializer(serializers.ModelSerializer):
    links = serializers.SerializerMethodField()
    class Meta:
        model = Image
        fields = ('id', 'name', 'links', 'created_at')
        read_only_fields = ('id', 'name', 'links', 'created_at')


    def get_links(self, obj: Image):
        return self.context['request'].build_absolute_uri(reverse("images-detail", args=[obj.id]))

class DetailImageSerializer(serializers.Serializer):
    thumbnail_urls = serializers.DictField(child=serializers.URLField(), required=False)
    original_image = serializers.URLField(required=False)
    expiring_binary_url = serializers.URLField(required=False)

class CreateImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('id', 'name', 'file', 'created_at')
        read_only_fields = ('id', 'created_at')