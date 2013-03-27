# -*- coding: utf-8 -*-

from datetime import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db import models
from utils import *
import logging

log = logging.getLogger('ffclub')


class ImageUpload(models.Model):
    """An image uploaded to an object using content type generic links."""

    usage = models.CharField(max_length=20,
                             choices=(('original', '原始圖'), ('preview', '預覽圖'), ('mobile', '行動版')),
                             default='original')

    description = models.CharField(max_length=255, verbose_name='相片說明')
    status = models.CharField(max_length=20,
                              choices=(('normal', '正常'), ('spam', '垃圾')),
                              default='normal')

    image_large = models.ImageField(upload_to=settings.FILE_PATH,
                                    width_field='image_large_width', height_field='image_large_height',
                                    max_length=255, db_index=True, verbose_name='相片檔案')

    create_user = models.ForeignKey(User, related_name='+')
    create_time = models.DateTimeField(default=datetime.now)

    content_type = models.ForeignKey(ContentType, related_name='images')
    entity_id = models.PositiveIntegerField()
    entity_object = generic.GenericForeignKey('content_type', 'entity_id')

    # Generated thumbnails

    image_medium = models.ImageField(upload_to=settings.FILE_PATH + '/m',
                                     width_field='image_medium_width', height_field='image_medium_height',
                                     max_length=255, db_index=True, null=True, blank=True)

    image_small = models.ImageField(upload_to=settings.FILE_PATH + '/s',
                                    width_field='image_small_width', height_field='image_small_height',
                                    max_length=255, db_index=True, null=True, blank=True)
    # Generated values
    image_large_width = models.IntegerField(null=True, blank=True)
    image_large_height = models.IntegerField(null=True, blank=True)

    image_medium_width = models.IntegerField(null=True, blank=True)
    image_medium_height = models.IntegerField(null=True, blank=True)

    image_small_width = models.IntegerField(null=True, blank=True)
    image_small_height = models.IntegerField(null=True, blank=True)

    def save(self):
        if self.id is None:

            image_name = self.image_large.name
            content_type = self.image_large.file.content_type
            image_stream = open_image(self.image_large)

            log.debug('Content Type: ' + content_type)

            large_size = compute_new_size((self.image_large_width, self.image_large_height),
                                          LARGE_SIZE, RESIZE_MODE_ASPECT_FILL)
            large_image = resize_image(image_name, image_stream, large_size, content_type)

            medium_size = compute_new_size((self.image_large_width, self.image_large_height),
                                           MEDIUM_SIZE, RESIZE_MODE_ASPECT_FIT)
            medium_image = resize_image(image_name, image_stream, medium_size, content_type)

            small_size = compute_new_size((self.image_large_width, self.image_large_height),
                                          SMALL_SIZE, RESIZE_MODE_ASPECT_FIT)
            small_image = resize_image(image_name, image_stream, small_size, content_type)

            self.image_medium.save(medium_image.name, medium_image, save=False)
            self.image_large.save(large_image.name, large_image, save=False)
            self.image_small.save(small_image.name, small_image, save=False)

        return super(ImageUpload, self).save()

    def __unicode__(self):
        return u'%s' % self.image_large.name
