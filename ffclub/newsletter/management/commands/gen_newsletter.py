# -*- coding: utf-8 -*-
from django.core.management.base import NoArgsCommand, BaseCommand
from ffclub.newsletter.utils import generate_newsletter


class Command(BaseCommand):
    help = 'Generate Newsletter Static Page'
    option_list = NoArgsCommand.option_list

    def handle(self, *args, **options):

        issue = args[0]
        generate_newsletter(issue)