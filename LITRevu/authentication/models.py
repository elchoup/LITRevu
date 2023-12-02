from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):

    profile_photo = models.ImageField(verbose_name='photo de profil')


class UserFollow(models.Model):
    user = models.ForeignKey(User,
                             related_name="following",
                             on_delete=models.CASCADE)
    followed_user = models.ForeignKey(User,
                                      related_name='followers',
                                      on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'followed_user')
