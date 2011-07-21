import string
import random
import re
import cgi

DEFAULT_LENGTH = <<RANDOM_STRING_LENGTH>>

def generate_random_string(length=DEFAULT_LENGTH, alphabet=string.lowercase+string.digits):
    """
    @return a random string of length @param length from alphabet @alphabet
    """
    return ''.join(random.choice(alphabet) for _ in xrange(length))

def first(items, test=lambda x: True):
    for item in items:
        if test(item):
            return item

    return None

def make_get_arguments(**kwargs):
    """
    Create dictionary into corresponding URL parameters
    """
    if not kwargs:
        return ''
    
    return '?' + '&'.join((
        '%s=%s' % (
            key,
            cgi.escape(str(value))
        )
        for key, value in kwargs.items()
    ))

def prepend_if_absent(prefix, text):
    if text.startswith(prefix):
        return
        
    return prefix + text

def is_substring_case_insensitive(text, substring):
    pattern = re.compile(substring, re.IGNORECASE)    
    

class EmailAddress(object):
    name_pattern = re.compile(
        r'\"?\s?'
        r'(?P<name>(:?[^ \s"]+\s?)+)?'
        r'\"?\s?'
    )

    email_pattern = re.compile(
        r'\<?'
        r'(?P<email>(?P<user>\w+)(:?\+(?P<contact>\w+))?@(?P<domain>(:?\w+\.)+\w+))'
        r'\>?\s?$'
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
        self.raw = original
        self.original = ' '.join(original.strip().lstrip().split())

        separator = self.original.rfind(' ') + 1
        
        m = self.name_pattern.search(self.original[:separator])
        self.name = m.group('name') or ''
        if self.name:
            self.name = self.name.strip()

        m = self.email_pattern.search(self.original[separator:])
        self.email = m.group('email') or ''
        self.user = m.group('user') or ''
        self.contact = m.group('contact') or ''
        self.domain = m.group('domain') or ''

    def __repr__(self):
        return "<EmailAddress '%s'>" % self.original
