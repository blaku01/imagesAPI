from django.db import models
from users.models import ImagesUser

# Create your models here.


class Image(models.Model):
    name = models.CharField(max_length=20)
    owner = models.ForeignKey(ImagesUser, on_delete=models.CASCADE)
    file = models.ImageField(upload_to="images/")
    created_at = models.DateTimeField(auto_now_add=True)
