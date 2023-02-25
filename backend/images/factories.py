import factory
from django.utils import timezone
from .models import Image
from users.factories import ImagesUserFactory

class ImageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Image

    name = factory.Sequence(lambda n: 'image{0}'.format(n))
    owner = factory.SubFactory(ImagesUserFactory)
    file = factory.django.ImageField(
        filename='test_image.jpg', 
        color='blue', 
        width=800, 
        height=600
    )
    created_at = factory.LazyFunction(timezone.now)