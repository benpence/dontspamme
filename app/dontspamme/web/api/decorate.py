import dontspamme.web.api.exception as exception

handler_method = lambda decorator: lambda method: lambda handler: decorator(handler, method)
handler_method_with_state = lambda decorator: lambda *args, **kwargs: lambda method: lambda handler: decorator(handler, method, *args, **kwargs)

@handler_method
def catch_errors(handler, method):
    """
    Verifies that the user is a member of this app
    Validates 'get' parameter 'p'
    Runs the post method (modifies the datastore)
    """    
    try:
        output = f()
    except APIError, e:
        logging.info(e)

        return json.dumps({
            'error': e
        })

    return json.dumps(output)

@handler_method
def is_admin(handler, method):
    """
    
    """
    member = handler.get_admin_member()
    if not member:
        raise exception.APIAuthorizationError()
    
    method(handler, member)

@handler_method    
def is_member(handler, method):
    """

    """
    member = handler.get_valid_member()
    if not member:
        raise exception.APIAuthorizationError()
    
    method(handler, member)

@handler_with_state
def read_options(handler, member, *exposed_arguments, **optional_filters):
    """
    Decorator for retriev
        exposed_arguments: tuple that contains attributes to be returned to client
        optional_filters: dictionary that specifies the requirements for optionally included filters (server side filtering)
    """
    received_arguments = handler.get_post_dict()
    
    for key, value in received_arguments:
        if key not in optionals:
            raise exception.APIMissingKeyError( , key)
        
        try:
            optionals[key] = optionals[key](value)
        except ValueError, e:
            raise exception.APIValueError()
            
    method(handler, member, *exposed_argumentsd, **optional_filters)

@handler_method_with_state
def write_options(handler, action, **requirements):
    received_arguments = handler.get_post_dict()

    for key, value in requirements:
        if key not in received_arguments:
            raise exception.APIMissingKeyError( , key)

        try:
            received_arguments[key] = requirements[key](value)

        except ValueError, e:
            raise exception.APIValueError( , key, requirement_type)

    action(handler, member, *args, **requirements)