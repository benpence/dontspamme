import string
import random
import re

DEFAULT_LENGTH = 16

def generate_random_string(length=DEFAULT_LENGTH, alphabet=string.letters+string.digits):
    """
    @return a random string of length @param length from alphabet @alphabet
    """
    return ''.join(random.choice(alphabet) for _ in xrange(length))

class EmailAddress(object):
    name_pattern = re.compile(
        r'\"?'
        r'(?P<name>.(:?[^ \s"]+\s*)+)?'
        r'\"?'
        r'\s*'
    )

    email_pattern = re.compile(
        r'\<?'
        r'(?P<email>(?P<user>\w+)(:?\+(?P<contact>\w+))?@(?P<domain>(:?\w+\.)+\w+))'
        r'\>?$'
    )
    
    def __init__(self, original):
        self.original = original

        separator = original.rfind(' ') + 1

        m = self.name_pattern.search(original[:separator])
        self.name = m.group('name')

        m = self.email_pattern.search(original[separator:])
        self.email = m.group('email')
        self.user = m.group('user')
        self.contact = m.group('contact')
        self.domain = m.group('domain')

    def __repr__(self):
        return "<EmailAddress '%s'>" % self.original
