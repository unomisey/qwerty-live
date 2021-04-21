from django.contrib.auth.models import User
from django.db import models


class QwertyProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follows = models.ManyToManyField('self', related_name='followed_by', symmetrical=False)
    avatar = models.ImageField(upload_to='uploads/', blank=True, null=True)


User.qwerterprofile = property(lambda u: QwertyProfile.objects.get_or_create(user=u)[0])