import exception

import random
random.seed()

def randomHash(length):
    """
    Return random hash with 'length' characters

    length:int -> str
    """

    """TODO: Evaluate different random functions in python by efficiency. Collision resistance is quite unimportant though"""
    
    return "%x" % random.getrandbits(length * 4)
    
def first(l, f):
    """
    Get first item in l that satisfies f(item) or None

    l:list | f:function -> _ or None
    """
    
    """TODO: Look up checking for iterables and functions"""
    if not (isinstance(l, list)):
        raise exception.InputError("list, function") 
    
    return next((n for n in l if f(n)), None)
    
def emailSplit(email, start='', end=''):
    """
    Returns rightmost string that is contained by start and end.
    """
    partition = email[email.rfind(start): email.rfind(end)]

    if not partition:
        return None

    return partition[1:]

def where(cls, count=0, **kwargs):
    results = cls.gql(
        "WHERE %s" % ' AND '.join(
            ("%s = :%s" % (key, key) for key in kwargs)
        ),
        **kwargs
    )

    if count:
        return results.fetch(count)

    return results
