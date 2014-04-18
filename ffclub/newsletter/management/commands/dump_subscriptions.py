# -*- coding: utf-8 -*-
from optparse import make_option
from django.core.management.base import BaseCommand
# import commonware.log

# log = commonware.log.getLogger('bedrock')
from ffclub.newsletter.models import Subscription


class Command(BaseCommand):
    help = 'Dump subscriptions from Database.'
    option_list = BaseCommand.option_list + (
        make_option('--all',
                    action='store_true',
                    dest='all',
                    default=False,
                    help='Dump all subscriptions.'),
    )

    def handle(self, *args, **options):
        if options['all']:
            subscriptions = Subscription.objects.all().exclude(email__isnull=True).exclude(email__exact='')
        else:
            subscriptions = Subscription.objects.filter(status=1).exclude(email__isnull=True).exclude(email__exact='')

        filename = 'subscriptions.txt'
        if args and len(args) > 0:
            filename = args[0]

        file = open(filename, 'w')
        for subscription in subscriptions:
            # print subscription.email.lower()
            file.write(subscription.email + '\n')
        file.close()
        print len(subscriptions)
