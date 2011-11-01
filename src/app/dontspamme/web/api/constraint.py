"""
Constraints for query values.
Return python-equivalent value from the str or raises an APIConstraintError with problem
"""
import re

from dontspamme.web.api import exception

DOMAIN_REGEX = re.compile('[a-zA-Z0-9_\-]+(\.[a-zA-Z0-9_\-]+)+')
def is_valid_domain(handler, key_name, domain):
    if not DOMAIN_REGEX.match(domain):
        raise exception.APIConstraintError(
            handler,
            key_name,
            "is not a valid domain"
        )
        
    return domain

EMAIL_REGEX = re.compile('[a-zA-Z0-9+_\-\.]+@[0-9a-zA-Z][.-0-9a-zA-Z]*.[a-zA-Z]+')
def is_valid_email(handler, key_name, address):
    if not EMAIL_REGEX.match(address):
        raise exception.APIConstraintError(
            handler,
            key_name,
            "is not a valid email address"
        )
    
    return address

def is_of_length(length):
    def correct_length(handler, key_name, value):
        try:
            if len(value) != length:
                raise exception.APIConstraintError(
                    handler,
                    key_name,
                    "is incorrect length"
                )
    
        except TypeError:
            raise exception.APIConstraintError(
                handler,
                key_name,
                "has incorrect type"
            )
            
        return value
        
    return correct_length
    
def is_boolean(handler, key_name, value):
    if value in ('True', 'true'):
        return True
    elif value in ('False', 'false'):
        return False
    
    raise exception.APIConstraintError(
        handler,
        key_name,
        "must be a boolean"
    )