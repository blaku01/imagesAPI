import tempfile
from io import BytesIO

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from django.urls import reverse
from faker import Faker
from freezegun import freeze_time
from images.models import Image
from images.tests.factories import ImageFactory
from PIL import Image as PILImage
from rest_framework import status
from rest_framework.test import APITestCase
from users.tests.factories import AccountTierFactory, ImagesUserFactory

from .helpers import get_test_image_file


@override_settings(MEDIA_ROOT=tempfile.mkdtemp())
class ImageCreateTestCase(APITestCase):
    def setUp(self):
        self.account_tier = AccountTierFactory(
            name="Enterprise",
            thumbnail_sizes=[200, 400, 600],
            original_file_link=True,
            expiring_link_enabled=False,
        )
        self.user = ImagesUserFactory()
        self.client.force_authenticate(user=self.user)
        self.faker = Faker()
        self.url = reverse("images-list")
        self.filename = "test_image"
        self.file = SimpleUploadedFile(
            name=self.filename + ".jpg",
            content=get_test_image_file().read(),
            content_type="image/jpeg",
        )

    def test_create_image_with_valid_jpg_image(self):
        data = {"name": self.filename, "file": self.file}
        response = self.client.post(self.url, data, format="multipart")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Image.objects.count(), 1)
        self.assertEqual(Image.objects.get().name, self.filename)
        self.assertEqual(Image.objects.get().owner, self.user)

    def test_create_image_with_valid_png_image(self):
        file = self.file
        file.name = self.filename + ".png"
        file.content_type = "image/png"
        data = {"name": self.filename, "file": file}
        response = self.client.post(self.url, data, format="multipart")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Image.objects.count(), 1)
        self.assertEqual(Image.objects.get().name, self.filename)
        self.assertEqual(Image.objects.get().owner, self.user)

    def test_create_image_with_missing_file(self):
        data = {"name": self.filename}
        response = self.client.post(self.url, data, format="multipart")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_image_with_invalid_name(self):
        data = {"name": "x" * 21, "file": self.file}
        response = self.client.post(self.url, data, format="multipart")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_image_with_non_image_file(self):
        # Create a non-image file (a text file) and create a SimpleUploadedFile object
        text_file = SimpleUploadedFile("text_file.txt", b"Text file contents.")

        # Create the request data with the non-image file
        data = {
            "name": self.filename,
            "file": text_file,
        }

        # Make the request to create a new image
        url = reverse("images-list")
        response = self.client.post(url, data, format="multipart")

        # Verify that the request was unsuccessful and that the image was not created
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Image.objects.count(), 0)

    def test_create_image_unauthorized(self):
        self.client.logout()
        data = {"name": self.filename, "file": self.file}
        response = self.client.post(self.url, data, format="multipart")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Image.objects.count(), 0)

    def test_create_image_without_name(self):
        data = {"file": self.file}

        response = self.client.post(self.url, data, format="multipart")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Image.objects.count(), 0)


@override_settings(MEDIA_ROOT=tempfile.mkdtemp())
class ImageLinkRetrievalTestCase(APITestCase):
    def setUp(self):
        account_tier = AccountTierFactory(expiring_link_enabled=True)
        self.user = ImagesUserFactory(account_tier=account_tier)
        self.client.force_authenticate(user=self.user)

    def test_retrieve_list_of_images(self):
        num_images = 5
        ImageFactory.create_batch(num_images, owner=self.user)
        url = reverse("images-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), num_images)
        for image in response.data:
            image_detail_url = reverse("images-detail", args=[image["id"]])
            self.assertEqual(image["url"], "http://testserver" + image_detail_url)
            response = self.client.get(image_detail_url, SERVER_NAME="testserver.com")
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_generate_image_urls(self):
        image = ImageFactory(owner=self.user)
        url = reverse("images-detail", args=[image.id])
        response = self.client.get(
            url + "?expiration_time=10", SERVER_NAME="testserver.com"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_response_keys = [
            "thumbnail_urls",
            "original_image",
            "expiring_binary_url",
        ]
        self.assertEqual(list(response.data.keys()), expected_response_keys)
        expected_thumbnail_keys = [
            "size_" + str(thumbnail_size)
            for thumbnail_size in self.user.account_tier.thumbnail_sizes
        ]
        self.assertEqual(
            list(response.data["thumbnail_urls"].keys()), expected_thumbnail_keys
        )

    def test_generate_different_user_image_urls(self):
        different_user = ImagesUserFactory()
        image = ImageFactory(owner=different_user)
        url = reverse("images-detail", args=[image.id])
        response = self.client.get(
            url + "?expiration_time=10", SERVER_NAME="testserver.com"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_generate_image_urls_without_expiring_url(self):
        image = ImageFactory(owner=self.user)
        url = reverse("images-detail", args=[image.id])
        response = self.client.get(url, SERVER_NAME="testserver.com")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_response_keys = ["thumbnail_urls", "original_image"]
        self.assertEqual(list(response.data.keys()), expected_response_keys)
        expected_thumbnail_keys = [
            "size_" + str(thumbnail_size)
            for thumbnail_size in self.user.account_tier.thumbnail_sizes
        ]
        self.assertEqual(
            list(response.data["thumbnail_urls"].keys()), expected_thumbnail_keys
        )


@override_settings(MEDIA_ROOT=tempfile.mkdtemp())
@freeze_time("2023-02-26")
class ImageShowTestCase(APITestCase):
    def setUp(self):
        account_tier = AccountTierFactory(expiring_link_enabled=True)
        self.user = ImagesUserFactory(account_tier=account_tier)
        self.client.force_authenticate(user=self.user)
        self.image = ImageFactory(
            owner=self.user,
            file=SimpleUploadedFile(
                "test.png",
                get_test_image_file(size=(200, 600)).read(),
                content_type="image/png",
            ),
        )
        urls = self.client.get(
            reverse("images-detail", args=[self.image.id]) + "?expiration_time=10",
            SERVER_NAME="testserver.com",
        ).data
        self.thumbnail_urls = urls["thumbnail_urls"]
        self.original_image_url = urls["original_image"]
        self.expiring_binary_image_url = urls["expiring_binary_url"]

    def test_return_thumbnail_images(self):
        for thumbnail_size, thumbnail_url in self.thumbnail_urls.items():
            thumbnail_size = thumbnail_size[5:]
            response = self.client.get(thumbnail_url, SERVER_NAME="testserver.com")
            image_data = response.content
            image = PILImage.open(BytesIO(image_data))
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(image._size[1], int(thumbnail_size))

    def test_return_original_image(self):
        response = self.client.get(
            self.original_image_url, SERVER_NAME="testserver.com"
        )
        original_image_data = response.content
        image = PILImage.open(BytesIO(original_image_data))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(image._size[0], self.image.file.width)
        self.assertEqual(image._size[1], self.image.file.height)

    def test_return_expiring_binary_image(self):
        response = self.client.get(
            self.expiring_binary_image_url, SERVER_NAME="testserver.com"
        )
        expiring_image_data = response.content
        image = PILImage.open(BytesIO(expiring_image_data))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(image._size[0], self.image.file.width)
        self.assertEqual(image._size[1], self.image.file.height)
        self.assertEqual(image.mode, "1")

    def test_wrong_signature(self):
        response = self.client.get(
            self.original_image_url[:-10] + "X" * 10, SERVER_NAME="testserver.com"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()["error"], "Invalid signature.")

    @freeze_time("2023-02-27")
    def test_image_expired(self):
        response = self.client.get(
            self.expiring_binary_image_url, SERVER_NAME="testserver.com"
        )
        self.assertEqual(response.status_code, status.HTTP_410_GONE)
        self.assertEqual(response.json()["error"], "Image expired.")
