from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic

from ffclub.event.models import Event
from ffclub.upload.models import ImageUpload


class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    quantity = models.IntegerField()
    photos = generic.GenericRelation(ImageUpload)

    def __unicode__(self):
        return unicode(self.title)


class Order(models.Model):

    usage = models.TextField(max_length=512)
    user = models.OneToOneField(User, primary_key=True)
    fullname = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    occupation = models.CharField(max_length=255)
    create_user = models.ForeignKey(User, related_name='+')
    create_time = models.DateTimeField(default=datetime.now)
    event = models.ForeignKey(Event, related_name='+')
    products = models.ManyToManyField(Product, related_name='+', through='OrderDetail')

    def __unicode__(self):
        return unicode(self.usage)


class OrderDetail(models.Model):

    description = models.CharField(max_length=255)
    quantity = models.IntegerField()
    order = models.ForeignKey(Order, related_name='details')
    product = models.ForeignKey(Product, related_name='+')

    def __unicode__(self):
        return unicode(self.quantity)

