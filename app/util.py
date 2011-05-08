import string
import random

def generate_random_string(length=32, alphabet=string.letters+string.digits):
    """
    @return a random string of length @param length from alphabet @alphabet
    """
    return ''.join(random.choice(alphabet) for _ in xrange(length))

def string_between(email, start='', end=''):
    """
    Returns rightmost string that is contained by start and end.
    """
    partition = email[email.find(start): email.rfind(end)]

    if not partition:
        return None
    
    return partition