from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from countries.models import Member

# Create your models here.


class LikedPlace(models.Model):
    user = models.ForeignKey(Member, on_delete=models.CASCADE)
    # Type (Country, State, Place)
    # Allow generic relationship using ID
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
