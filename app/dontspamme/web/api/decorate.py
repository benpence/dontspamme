import dontspamme.web.api.exception as exception

def stateless_decorator(decorator):
    """
    Decorator that does not take arguments
        Allows stacking on an instance method
    """
    def decorator_replacement(decorated_method):
        def instance_method(self, *instance_args, **instance_kwargs):
            decorator(*((self, decorated_method) + instance_args), **instance_kwargs.items())
        return instance_method
    return initialized_decorator

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
    member = handler.get_admin_member()
    if not member:
        raise exception.APIAuthorizationError()
    
    method(handler, member)

@stateless_decorator    
def is_member(handler, method):
    member = handler.get_valid_member()
    if not member:
        raise exception.APIAuthorizationError()
    
    method(handler, member)

@stateful_decorator
def read_options(handler, method, member, *exposed_arguments, **optional_filters):
    """
    Decorator for retrieving objects from the database
    
    Args:
        exposed_arguments: tuple that contains attributes to be returned to client
        optional_filters: dictionary that specifies the requirements for optionally included filters (server side filtering)
    """
    received_arguments = handler.get_post_dict()
    
    for key, value in received_arguments:
        if key not in optional_filters:
            raise exception.APIMissingKeyError( , key)
        
        try:
            optional_filters[key] = optional_filters[key](value)
        except ValueError:
            raise exception.APIValueError(key, optional_filters[key])
            
    method(handler, member, *exposed_arguments, **optional_filters)

@stateful_decorator
def write_options(handler, method, member, **requirements):
    """
    Args:
        requirements: dict of argument name to a method that checks and converts its type for accessing/modifying the app
    """
    received_arguments = handler.get_post_dict()

    for key, value in requirements:
        if key not in received_arguments:
            raise exception.APIMissingKeyError( , key)

        try:
            received_arguments[key] = requirements[key](value)
        except ValueError:
            raise exception.APIValueError(key, requirements[key])

    method(handler, member, **requirements)