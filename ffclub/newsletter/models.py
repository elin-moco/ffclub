from datetime import datetime
from django.db import models


class Newsletter(models.Model):
    title = models.TextField(blank=False)
    issue = models.DateField(blank=False)
    volume = models.IntegerField(default=1)
    publish_date = models.DateField(default=datetime.now)

    class Meta:
        db_table = u'issue'


class Subscription(models.Model):
    u_email = models.TextField(blank=False)
    u_status = models.IntegerField(default=1)
    edit_date = models.DateField(default=datetime.now)

    class Meta:
        db_table = u'newsletter'


class NewsletterRouter(object):
    """
    A router to control all database operations on models in the
    auth application.
    """
    def db_for_read(self, model, **hints):
        """
        Attempts to read auth models go to auth_db.
        """
        if model._meta.app_label == 'newsletter':
            return 'newsletter'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write auth models go to auth_db.
        """
        if model._meta.app_label == 'newsletter':
            return 'newsletter'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the auth app is involved.
        """
        if obj1._meta.app_label == 'newsletter' or \
           obj2._meta.app_label == 'newsletter':
            return True
        return None

    def allow_migrate(self, db, model):
        """
        Make sure the auth app only appears in the 'auth_db'
        database.
        """
        if db == 'newsletter':
            return model._meta.app_label == 'newsletter'
        elif model._meta.app_label == 'newsletter':
            return False
        return None