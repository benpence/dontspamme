_HASH_LENGTH = 12

import random
random.seed()

def random_hash():
    """
    None -> str
    """
    
    return "%x" % random.getrandbits(_HASH_LENGTH * 4)