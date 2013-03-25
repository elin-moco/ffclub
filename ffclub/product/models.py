# -*- coding: utf-8 -*-
from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic

from ffclub.event.models import Event
from ffclub.upload.models import ImageUpload


class Product(models.Model):
    title = models.CharField(max_length=255, verbose_name='品名')
    description = models.CharField(max_length=255, verbose_name='描述')
    quantity = models.IntegerField(verbose_name='數量')
    photos = generic.GenericRelation(ImageUpload, content_type_field='content_type', object_id_field='entity_id')

    def __unicode__(self):
        return unicode(self.title)


class Order(models.Model):

    usage = models.TextField(max_length=512, verbose_name='用途說明')
    fullname = models.CharField(max_length=255, verbose_name='姓名')
    email = models.EmailField()
    address = models.CharField(max_length=255, verbose_name='地址')
    occupation = models.CharField(max_length=255, verbose_name='職業', blank=True, default='')
    create_user = models.ForeignKey(User, related_name='+')
    create_time = models.DateTimeField(default=datetime.now)
    event = models.ForeignKey(Event, related_name='+')
    products = models.ManyToManyField(Product, related_name='+', through='OrderDetail')
    status = models.CharField(max_length=20,
                              choices=(('wait_for_confirm', '待確認'), ('confirmed', '已確認')),
                              default='wait_for_confirm')

    def __unicode__(self):
        return unicode(self.usage)


class OrderDetail(models.Model):

    description = models.CharField(max_length=255)
    quantity = models.IntegerField()
    order = models.ForeignKey(Order, related_name='details')
    product = models.ForeignKey(Product, related_name='+')

    def __unicode__(self):
        return unicode(self.quantity)


class OrderVerification(models.Model):

    code = models.CharField(max_length=255)
    create_user = models.ForeignKey(User, related_name='+')
    create_time = models.DateTimeField(default=datetime.now)
    status = models.CharField(max_length=20,
                              choices=(('issued', '待確認'), ('confirmed', '已確認')),
                              default='issued')
    order = models.ForeignKey(Order, related_name='+')

    def __unicode__(self):
        return unicode(self.quantity)
