from typing import Any
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class TaggedPlaceManager(models.Manager):
    def get_tags_for(self, obj_type, obj_id):
        content_type = ContentType.objects.get_for_model(obj_type)
        return TaggedPlace.objects \
            .select_related('tag') \
            .filter(
                content_type=content_type,
                object_id=obj_id
            )

    def get_places_for(self, obj_type, obj_id):
        content_type = ContentType.objects.get_for_model(obj_type)
        return TaggedPlace.objects \
            .values(place_id=models.F('object_id')) \
            .filter(
                content_type=content_type,
                tag_id=obj_id
            )


class Tag(models.Model):
    label = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.label


class TaggedPlace(models.Model):
    objects = TaggedPlaceManager()
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    # Type (Country, State, Place)
    # Allow generic relationship using ID
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
