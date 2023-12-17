from django.core.validators import MinValueValidator
from django.core.validators import MaxValueValidator, FileExtensionValidator
from django.db import models
from django.conf import settings
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile


class Ticket(models.Model):
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=2048, blank=True)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    image = models.ImageField(upload_to='static/images/',
                              null=True, blank=True,
                              validators=[FileExtensionValidator(
                                  allowed_extensions=['jpg', 'jpeg', 'png'])])
    time_created = models.DateTimeField(auto_now_add=True)

    IMAGE_MAX_SIZE = (800, 800)

    def resize_image(self):
        if self.image:
            img = Image.open(self.image.path)
            img.thumbnail(self.IMAGE_MAX_SIZE)

            img_io = BytesIO()
            img.save(img_io, format='JPEG')
            img_file = ContentFile(img_io.getvalue(),
                                   name=f"{self.image.name}")

            # Enregistrez l'image redimensionnée dans le modèle
            self.image.save(f"{self.image.name}", img_file, save=False)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.resize_image()


class Review(models.Model):
    ticket = models.OneToOneField(Ticket, on_delete=models.CASCADE,
                                  related_name='review')
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    headline = models.CharField(max_length=128)
    body = models.CharField(max_length=8192, blank=True)
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    time_created = models.DateTimeField(auto_now_add=True)
