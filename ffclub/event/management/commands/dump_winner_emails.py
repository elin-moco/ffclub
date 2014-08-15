# -*- coding: utf-8 -*-
from django.core.management.base import NoArgsCommand, BaseCommand
from ffclub.event.models import Campaign, Award


class Command(BaseCommand):
    help = 'Dump campaign winners'
    option_list = NoArgsCommand.option_list

    def handle(self, *args, **options):
        self.options = options
        if args and len(args) > 0:
            campaign_slug = args[0]
            current_campaign = Campaign.objects.get(slug=campaign_slug)
            random_awards = Award.objects.filter(name=u'隨機抽獎', activity=current_campaign).order_by('order')

            filename = 'winners.txt'
            if args and len(args) > 1:
                filename = args[1]

            f = open(filename, 'w')
            for award in random_awards:
                f.write(award.winner_extra + '\n')
            f.close()
        else:
            print 'Campaign slug required'