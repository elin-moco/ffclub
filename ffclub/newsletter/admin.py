from ffclub.base import admin
from django.contrib.admin import ModelAdmin
from .models import *


class NewsletterAdmin(ModelAdmin):
    search_fields = ['title']
    list_filter = ['issue', 'volume', 'publish_date']

admin.site.register(Newsletter, NewsletterAdmin)


class SubscriptionAdmin(ModelAdmin):
    search_fields = ['email']
    list_filter = ['edit_date', 'status']

admin.site.register(Subscription, SubscriptionAdmin)


