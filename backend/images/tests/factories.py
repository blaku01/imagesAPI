import factory
from django.utils import timezone
from ..models import Image
from users.tests.factories import ImagesUserFactory
from django.core.files.base import ContentFile
from django.core.files.images import ImageFile
from faker import Faker
from .helpers import get_test_image_file
from django.core.files.uploadedfile import SimpleUploadedFile

fake = Faker()

class ImageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Image

    name = factory.Sequence(lambda n: 'image{0}'.format(n))
    owner = factory.SubFactory(ImagesUserFactory)
    file = SimpleUploadedFile('test.png', get_test_image_file().read(), content_type='image/png')
    created_at = factory.LazyFunction(timezone.now)