import os
import string


def generate_random_string(length, string_set=string.ascii_letters + string.digits + string.punctuation):
    """
    Returns a string with `length` characters chosen from `string_set`
    >>> len(generate_random_string(20)) == 20
    """
    return ''.join([string_set[i%len(string_set)] \
                    for i in [ord(x) for x in os.urandom(length)]])