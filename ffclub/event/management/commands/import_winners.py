# -*- coding: utf-8 -*-
import re
from django.core.management.base import NoArgsCommand, BaseCommand
# import commonware.log

# log = commonware.log.getLogger('bedrock')
from ffclub.newsletter.utils import newsletter_subscribe
from ffclub.event.models import Award, Campaign

email_re = re.compile('^[_A-z0-9-]+(\.[_A-z0-9-]+)*@[A-z0-9-]+(\.[A-z0-9-]+)*(\.[A-z]{2,4})$')


class Command(BaseCommand):
    help = 'Import subscriptions to Database.'
    option_list = NoArgsCommand.option_list

    def handle(self, *args, **options):
        self.options = options
        filename = 'winners.txt'
        if args:
            if len(args) > 0:
                campaign = Campaign.objects.get(slug=args[0])
                if len(args) > 1:
                    filename = args[1]
                with open(filename, 'r') as file:
                    subscriptions = file.readlines()
                    count = 0
                    for subscription in subscriptions:
                        email = subscription.strip()
                        if email_re.match(email):
                            award = Award(name=u'抽獎', activity=campaign, winner_extra=email)
                            award.save()
                            count += 1
                        else:
                            print 'Invalid email: %s' % email
                        # file.write(subscription.u_email + '\n')
                    file.close()
                    print '%d awards.' % count
