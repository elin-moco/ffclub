# -*- coding: utf-8 -*-
from django.core.management.base import NoArgsCommand, BaseCommand
import sys

import commonware.log
from ffclub.newsletter.utils import send_newsletter

log = commonware.log.getLogger('newsletter')


class Unbuffered:

    def __init__(self, stream):
        self.stream = stream

    def write(self, data):
        self.stream.write(data)
        self.stream.flush()

    def __getattr__(self, attr):
        return getattr(self.stream, attr)

class Command(BaseCommand):
    help = 'Send Newsletter'
    option_list = NoArgsCommand.option_list

    def handle(self, *args, **options):
        self.options = options
        testing = True if 1 < len(args) else False
        sys.stdout = Unbuffered(sys.stdout)
        issue_number = args[0]
        send_newsletter(issue_number, args[1], testing)
