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
        """
        Args:
            original: InboundEmailMessage

        Regex fields:
            name: The string in quotes at the beginning
            email: Full email (without the quotes part)
                user: Before the last '+'
                contact: After the last '+' but before the '@'
                domain: After the '@'
        """
        self.original = original

        separator = original.rfind(' ') + 1

        m = self.name_pattern.search(original[:separator])
        self.name = m.group('name') or ''

        m = self.email_pattern.search(original[separator:])
        self.email = m.group('email') or ''
        self.user = m.group('user') or ''
        self.contact = m.group('contact') or ''
        self.domain = m.group('domain') or ''

    def __repr__(self):
        return "<EmailAddress '%s'>" % self.original
