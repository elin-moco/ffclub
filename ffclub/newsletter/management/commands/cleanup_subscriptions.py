# -*- coding: utf-8 -*-
from django.core.management.base import NoArgsCommand, BaseCommand
# import commonware.log

# log = commonware.log.getLogger('bedrock')
from django.db.models import Count
from ffclub.newsletter.models import Subscription


class Command(BaseCommand):
    help = 'Cleanup subscriptions from Database.'
    option_list = NoArgsCommand.option_list

    def handle(self, *args, **options):
        self.options = options
        subscriptions = Subscription.objects.exclude(
            email__regex='^[_A-z0-9-]+(\.[_A-z0-9-]+)*@[A-z0-9-]+(\.[A-z0-9-]+)*(\.[A-z]{2,4})$')
        print 'Found %d invalid subscriptions.' % len(subscriptions)
        for subscription in subscriptions:
            subscription.delete()

        duplicates = Subscription.objects.values('email').annotate(count=Count('id')).order_by().filter(count__gt=1)
        print duplicates
        duplicateEmails = Subscription.objects.filter(email__in=[item['email'] for item in duplicates]).order_by('email')
        print 'Found %d duplicate subscriptions.' % len(duplicateEmails)

        previousEmail = None
        for duplicateEmail in duplicateEmails:
            currentEmail = duplicateEmail.email.lower()
            if previousEmail == currentEmail:
                print 'duplicate: %s' % currentEmail
                duplicateEmail.delete()
            previousEmail = currentEmail