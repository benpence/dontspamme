import exception

import random
random.seed()

def random_hash(length):
    """
    length:int -> str
    
    Return random hash with 'length' characters
    """

    """TODO: Evaluate different random functions in python by efficiency. Collision resistance is quite unimportant though"""
    
    return "%x" % random.getrandbits(length * 4)
    
def first(l, f):
    """
    l:list | f:function -> _ or None
    
    Get first item in l that satisfies f(item) or None
    """
    
    """TODO: Look up checking for iterables and functions"""
    if not (isinstance(l, list)):# or not isinstance(f, callable):
        raise exception.InputError("list, function") 
    
    return next((n for n in l if f(n)), None)
    
def email_split(email, start='', end=''):
    partition = email[email.rfind(start): email.rfind(end)]

    if not partition:
        return None

    return partition[1:]
