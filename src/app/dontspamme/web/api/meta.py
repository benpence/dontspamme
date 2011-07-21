import logging
from types import FunctionType

from dontspamme.web.api import exception

CHILD_METHODS_NAME = '<<CHILD_METHODS_NAME>>'
def get(self):
    """
    Catches errors in get requests and reports them to client on 'get' requests
    """
    try:
        self.read()

    # APIErrors are caught    
    except exception.APIError as e:
        logging.debug(e)
        return self.error(e.value)
    
    # No read method
    except TypeError:
        return self.error("This object cannot be read")

    # Construct results tree
    self.writeout(
        self.make_results_tree(*self.output)
    )
    
def post(self, action):
    child_methods = getattr(self, CHILD_METHODS_NAME)
    if action not in child_methods:
        return self.error("Invalid action '%s'" % action)

    # Modify object    
    try:
        child_methods[action](self)

    # APIErrors are caught
    except exception.APIError, e:
        logging.debug(e)
        return self.error(e)
    
    # No results returned
    self.writeout({'message': 'Completed successfully'})

class APIHandlerFactory(type):
    """
    Saves child methods as a dictionary attribute in the child class
    Metaclass redirects post requests to the appropriate method in the handler
    """
    def __new__(meta, name, parents, attributes):
        attributes[CHILD_METHODS_NAME] = dict((
            (attribute_name, attribute)
            for attribute_name, attribute in attributes.items()
            if type(attribute) == FunctionType and not attribute_name.startswith('__') and attribute != 'read'
        ))
        
        attributes['post'] = post
        attributes['get'] = get
        
        return type.__new__(meta, name, parents, attributes)        