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
    pattern = re.compile(
        # Name
        r'\"?'
        r'(?P<name>.(:?\w+\s*)+)?'
        r'\"?'

        r'\s*'

        # Email address
        r'\<?(?P<email>(?P<user>\w+)(:?\+(?P<contact>\w+))?@(?P<domain>(:?\w+\.)+\w+))'
        r'\>?$'
    )
    
    def __init__(self, raw):
        self.raw = raw

        m = self.pattern.search(raw)

        self.name = m.group('name')
        self.email = m.group('email')
        self.user = m.group('user')
        self.contact = m.group('contact')
        self.domain = m.group('domain')

    def __repr__(self):
        return self.raw
