class Error(Exception):
    def __init__(self, value):
        self.value = value
        
    def __str__(self):
        return repr(self.value)

class InputError(Error):
    """
    A function's input is invalid so we can nip problems in the bud without tracing down stupid errors.
    """
    
    def __str__(self):
        return 'Invalid input arguments. Expects (' + self.value + ')'

class EmptyQueryError(Error):
    """
    The datastore has returned nothing, even though there totally should be something.
    """
