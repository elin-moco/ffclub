import os
import string
from threading import Thread
from email.errors import MessageError
import logging

log = logging.getLogger('ffclub')


def generate_random_string(length, string_set=string.ascii_letters + string.digits + string.punctuation):
    """
    Returns a string with `length` characters chosen from `string_set`
    >>> randomString = generate_random_string(20, string.ascii_letters)
    >>> len(randomString) == 20
    True
    >>> set(randomString) < set(string.ascii_letters)
    True
    """
    return ''.join([string_set[i % len(string_set)]
                    for i in [ord(x) for x in os.urandom(length)]])


class MailThread(Thread):

    def __init__(self, mail=None):
        if mail is not None:
            self.mail = mail
        super(MailThread, self).__init__()

    def run(self):
        if self.mail is not None:
            try:
                self.mail.send()
            except MessageError as e:
                log.debug('Failed to send verification mail: ', e)
            except RuntimeError as e:
                log.debug('Unexpected error when sending verification mail: ', e)


