"""
Decorators for describing handler functions.
"""

from dontspamme.web.api import exception

def stateless_decorator(decorator):
    """
    Decorator that does not take arguments
        Allows stacking on an instance method
    """
    def decorator_replacement(decorated_method):
        def instance_method(self, *instance_args, **instance_kwargs):
            decorator(*((self, decorated_method) + instance_args), **instance_kwargs)
        return instance_method
    return decorator_replacement

def stateful_decorator(decorator):
    """
    Decorator that takes arguments
        Allows stacking on an instance method
        Arguments passed to the decorator method come before the initialization args/kwargs
    """
    def uninitialized_decorator(*dec_args, **dec_kwargs):
        def initialized_decorator(decorated_method):
            def instance_method(self, *instance_args, **instance_kwargs):
                decorator(*((self, decorated_method) + instance_args + dec_args), **dict(instance_kwargs.items() + dec_kwargs.items()))
            return instance_method
        return initialized_decorator
    return uninitialized_decorator

@stateless_decorator
def is_admin(handler, method):
	"""
	Requires that the member (not Google user) is an admin.
	"""
    member = handler.get_admin_member()
    if not member:
        raise exception.APIAuthorizationError()
    
    method(handler, member)

@stateless_decorator    
def is_member(handler, method):
	"""
	Requires app membership.
	"""
    member = handler.get_valid_member()
    if not member:
        raise exception.APIAuthorizationError()
    
    method(handler, member)

@stateful_decorator
def read_options(handler, method, member, *exposed_arguments, **optional_filters):
    """
    Decorator for retrieving objects from the database
    
    Args:
        exposed_arguments {tuple}: contains attributes to be returned to client
        optional_filters {dict}: that specifies the requirements for optionally included filters (server side filtering)
    """
    received_arguments = handler.get_post_dict()
    filters = {}
    
    for key, value in optional_filters.items():
        if key not in received_arguments:
            continue
        
        try:
            filters[key] = optional_filters[key](handler, key, received_arguments[key])
        except ValueError:
            raise exception.APIValueError(handler_name, key, optional_filters[key])
            
    method(handler, member, *exposed_arguments, **filters)

@stateful_decorator
def write_options(handler, method, member, **requirements):
    """
    Args:
        requirements {dict}: argument_name => constraint_method, checks and converts its type for accessing/modifying the app
    """
    received_arguments = handler.get_post_dict()

    for key, value in requirements.items():
        if key not in received_arguments:
            raise exception.APIMissingKeyError(handler, key)

        try:
            received_arguments[key] = requirements[key](value)
        except ValueError:
            raise exception.APIValueError(handler, key, requirements[key])

    method(handler, member, **requirements)