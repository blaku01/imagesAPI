from django.urls import path, include
from rest_framework import routers
from .views import ImageViewSet, ShowImageView

router = routers.SimpleRouter()

urlpatterns = [
    path('', include(router.urls)),
]

urlpatterns += router.urls
