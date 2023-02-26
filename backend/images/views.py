from django.core.signing import BadSignature, Signer
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils import timezone
from images.serializers import (
    CreateImageSerializer,
    DetailImageSerializer,
    ListImageSerializer,
)
from PIL import Image as PilImage
from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import AccountTier
from rest_framework.decorators import action
from .models import Image


class ImageViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Image.objects.filter(owner=self.request.user)
        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return ListImageSerializer
        elif self.action == "generate_image_variants":
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
        return Response(instance_serializer.data, status=201)

    def retrieve(self, request: HttpRequest, pk=None):
        try:
            request_url = request.build_absolute_uri()
            Signer(sep="&signature=").unsign(request_url)
        except BadSignature:
            return Response(status=400, data={"error": "Invalid signature."})

        image = get_object_or_404(Image.objects.all(), pk=pk)
        image = PilImage.open(image.file.path)
        format = image.format
        content_type = "image/" + format.lower()
        response = HttpResponse(content_type=content_type)
        if request.query_params.get("expires_at"):
            expires_at = float(request.query_params.get("expires_at"))
            if expires_at < timezone.now().timestamp():
                return Response(status=410, data={"error": "Image expired."})
            image = image.convert("1")

        elif "height" in request.query_params:
            height = int(request.query_params.get("height"))
            aspect_ratio = image.size[0] / image.size[1]
            image = image.resize((int(aspect_ratio * height), height), PilImage.NEAREST)

        image.save(response, format)

        return response

    @action(detail=True, url_name="variants")
    def generate_image_variants(self, request: HttpRequest, pk=None):
        signer = Signer(sep="&signature=")
        image = get_object_or_404(self.get_queryset(), pk=pk)
        serializer = self.get_serializer_class()
        account_tier: AccountTier = request.user.account_tier
        response = {}
        thumbnail_urls = {}
        url = request.build_absolute_uri(reverse("images-detail", args=[image.id]))

        for thumbnail_size in account_tier.thumbnail_sizes:
            thumbnail_urls["size_" + str(thumbnail_size)] = signer.sign(
                f"{url}?height={thumbnail_size}"
            )
        response["thumbnail_urls"] = thumbnail_urls

        if account_tier.original_file_link:
            response["original_image"] = signer.sign(f"{url}?original=True")

        if account_tier.expiring_link_enabled and request.query_params.get(
            "expiration_time", 0
        ):
            expiration_time = int(request.query_params.get("expiration_time"))
            expires_at = (
                timezone.now() + timezone.timedelta(seconds=expiration_time)
            ).timestamp()
            response["expiring_binary_url"] = signer.sign(
                f"{url}?expires_at={expires_at}"
            )
        serialized_data = serializer(data=response)
        serialized_data.is_valid(raise_exception=True)
        return Response(serialized_data.data)

