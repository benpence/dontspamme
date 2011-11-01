"""
When these errors are raised, the handler returns the message to the client.
"""

class APIError(Exception):
    def __init__(self, value):
        self.value = value
        
    def __str__(self):
        return repr(self.value)

class APIAuthorizationError(APIError):
    """User unauthorized to perform that action"""
    def __init__(self):
        self.value = "Unauthorized request"

class APIMissingKeyError(APIError):
    """Required key missing from request"""
    def __init__(self, handler, key_name):
        self.value = "%s requires the attribute '%s'" % (
            handler.__class__.__name__,
            key_name
        )
    
class APIValueError(APIError):
    """Passed value did not match expected value type"""
    def __init__(self, handler, key_name, value_type):
        self.value = "%s: '%s' attribute must be '%s'" % (
            key_name,
            value_type.__name__
        )
        
class APIConstraintError(APIError):
    """Passed value did not comply with extra constraints"""
    def __init__(self, handler, key_name, message):
        self.value = "%s: '%s' attribute %s" % (
            handler.__class__.__name__,
            key_name,
            message
        )
                
class APINoKeyError(APIError):
    def __init__(self, handler):
        self.value = "%s: value not found" % handler.__class__.__name__