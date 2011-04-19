import exception

import random
random.seed()

def random_hash(length):
    """
    Return random hash with 'length' characters

    length:int -> str
    """

    # TODO: Evaluate different random functions in python by efficiency.
    # Collision resistance is quite unimportant though
    
    return "%x" % random.getrandbits(length * 4)
    
def first(l, f):
    """
    Get first item in l that satisfies f(item) or None

    l:list | f:function -> _ or None
    """
    
    # TODO: Look up checking for iterables and functions
    if not (isinstance(l, list)):
        raise exception.InputError("list, function") 
    
    return next((n for n in l if f(n)), None)
