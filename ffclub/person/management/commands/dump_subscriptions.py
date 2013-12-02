# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.core.management.base import NoArgsCommand, BaseCommand


class Command(BaseCommand):
    help = 'Generate share images'
    option_list = NoArgsCommand.option_list

    def handle(self, *args, **options):
        self.options = options
        subscriptions = User.objects.filter(person__subscribing=True)
        for subscription in subscriptions:
            print subscription.email
