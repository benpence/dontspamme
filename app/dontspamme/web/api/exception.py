class Error(Exception):
    def __init__(self, value):
        self.value = value
        
    def __str__(self):
        return repr(self.value)


class APIError(Error):
    pass
    
class APIMissingKeyError(APIError):
    """Required key missing from request"""
    def __init__(self, object_name, key_name):
        self.value = "%s: requires the attribute '%s'" % (
            object_name,
            key_name
        )

class APIValueError(APIError):
    """Passed value did not match expected value type"""
    def __init__(self, object_name, key_name, value_type):
        self.value = "%s: expects '%s' to be '%s'" % (
            object_name,
            key_name,
            value_type
        )

class APIValueConstraintError(APIError):
    """Passed value did not comply with extra constraints"""
    def __init__(self, message):
        self.value = message
        
class APIAuthorizationError(APIError):
    """User unauthorized to perform that action"""
    def __init__(self):
        self.value = "Unauthorized request"
        
class APINoKeyError(APIError):
    def __init__(self, object_name):
        self.value = "%s: key is not valid" % object_name