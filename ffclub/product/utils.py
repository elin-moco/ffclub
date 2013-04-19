# -*- coding: utf-8 -*-
import os
import string
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
