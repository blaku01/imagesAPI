from django.urls import include, path
from rest_framework import routers

from .views import ImageViewSet

router = routers.SimpleRouter()
router.register(r"images", ImageViewSet, "images")

urlpatterns = [
    path("", include(router.urls)),
]

urlpatterns += router.urls
