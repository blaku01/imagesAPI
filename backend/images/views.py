from images.serializers import (CreateImageSerializer, DetailImageSerializer,
                                ListImageSerializer)
from rest_framework import permissions, viewsets
from rest_framework.response import Response

from .models import Image

# Create your views here.


class ImageViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Image.objects.filter(owner=self.request.user)
        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return ListImageSerializer
        elif self.action == "retrieve":
            return DetailImageSerializer
        else:
            return CreateImageSerializer

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)
        instance_serializer = ListImageSerializer(
            instance, context={"request": request}
        )
        return Response(instance_serializer.data)

    """
        TODO: CREATE retrieve() function, which will return data formatted like: 
        {'thumbnail_urls':[<urls>], 'original_image':<url>, 'expiring_binary_url':<url>}
    """
