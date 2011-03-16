class Error(Exception):
    def __init__(self, value):
        self.value = value
        
    def __str__(self):
        return repr(self.value)

class InputError(Error):
    """
    Called when a function's input is 
    """
    
    def __str__(self):
        return 'Invalid input arguments. Expects (' + self.value + ')'
        
