from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuarios(AbstractUser):

    imagem = models.ImageField(
        upload_to='usuarios/',
        blank=True,
        null=True
    )