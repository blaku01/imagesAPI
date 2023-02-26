from django.urls import include, path
from rest_framework import routers

from .views import ImageViewSet, ShowImageView

router = routers.SimpleRouter()
router.register(r"images", ImageViewSet, "images")

urlpatterns = [
    path("view/<int:pk>", ShowImageView.as_view(), name="show-image-view"),
    path("", include(router.urls)),
]

urlpatterns += router.urls
