from types import FunctionType

CHILD_METHODS_NAME = '<<CHILD_METHODS_NAME>>'

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
        
        attributes['post'] = meta.post
        attributes['get'] = meta.get
        
        return type.__new__(meta, name, parents, attributes)        
        
    def get(self):
        """
        Catches errors in get requests and reports them to client on 'get' requests
        """
        try:
            results, exposed_values = self.read()

        # APIErrors are caught    
        except APIError as e:
            logging.debug(e.value)
            return self.error(e.value)
        
        # No read method
        except AttributeError:
            return self.error("This object cannot be read")

        # Construct results tree
        self.writeout(
            self.make_results_tree(results, exposed_values)
        )
        
    def post(self, action):
        child_methods = getattr(self, CHILD_METHODS_NAME)
        if action not in child_methods:
            return self.error("Invalid action '%s'" % action)

        # Modify object    
        try:
            results, exposed_values = child_methods[action](self)

        # APIErrors are caught
        except APIError, e:
            logging.debug(e)
            return self.error(e)
        
        # No results returned
        except TypeError:
            return self.writeout({'message': 'Completed successfully'})
            
            
        self.writeout(
            self.make_results_tree(results, exposed_values)
        )