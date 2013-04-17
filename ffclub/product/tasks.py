from email.errors import MessageError
from celery.task import task
import logging

log = logging.getLogger('ffclub')

@task()
def send_mail(mail):
    if mail is not None:
        try:
            mail.send()
        except MessageError as e:
            log.debug('Failed to send verification mail: ', e)
        except RuntimeError as e:
            log.debug('Unexpected error when sending verification mail: ', e)
