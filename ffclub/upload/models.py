from datetime import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db import models


class ImageUpload(models.Model):
    """An image uploaded to an object using content type generic links."""

    description = models.CharField(max_length=255)

    data_file = models.ImageField(upload_to=settings.FILE_PATH, max_length=255, db_index=True)

    create_user = models.ForeignKey(User, related_name='+')
    create_time = models.DateTimeField(default=datetime.now)

    content_type = models.ForeignKey(ContentType, related_name='images')
    entity_id = models.PositiveIntegerField()
    entity_object = generic.GenericForeignKey('content_type', 'entity_id')

    def __unicode__(self):
        return u'%s' % self.data_file.name

class ImageUploadPool(models.Model):
    """Image working pool for post writing, will move to ImageUpload later."""

    data_file = models.ImageField(upload_to=settings.FILE_PATH, max_length=255, db_index=True)
    create_user = models.ForeignKey(User, related_name='+')
    create_time = models.DateTimeField(default=datetime.now)

