# -*- coding: utf-8 -*-

import logging

from celery.task import task

from ffclub.settings import SUBSCRIBER_EMAILS_PATH
from ffclub.person.models import Person


log = logging.getLogger('ffclub')


@task()
def export_subscriber_emails():
    file = open(SUBSCRIBER_EMAILS_PATH, 'w')
    people = Person.objects.filter(subscribing=True)
    for person in people:
        file.write(person.user.email)
        file.write('\n')
    file.close()
