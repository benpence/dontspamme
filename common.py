import random
random.seed()

def random_hash(length):
    """
    length:int -> str
    
    Return random hash with 'length' characters
    """
    
    return "%x" % random.getrandbits(length * 4)
    
    
def first(l, f):
    """
    l:[_] | f:function -> _ or None
    
    Get first item in l that satisfies f(item) or None
    """
    
    return next((n for n in l if f(n)), None)