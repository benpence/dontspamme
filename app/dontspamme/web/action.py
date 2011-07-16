import cgi
import logging

import dontspamme.util as util
import dontspamme.model as model
from dontspamme.web.authenticate import AuthenticatedRequest

class confirm_get(object):
    """
    Request decorator
        Verifies that the user is a member of this app
        Creates dict of get variables
        Runs the get method (retrieve data for confirmation template if necessary)
        Renders the confirmation template
    """
    def __init__(self, action, format_string):
        self.action = action
        self.format_string = format_string

    def __call__(self, get_method):
        def wrapper(handler):
            """
            URL in the format domain/action?p=X
            """
            user = handler.get_valid_user()
            if not user:
                return handler.home()
            
            variables = handler.get_post_dict()
            """
            Run get method
            Allow get method to 'break out' of response by returning False
            Params:
                user: current Google user
                variables: dict of get variables
            """
            if get_method(handler, user, variables) == False:
                return handler.home()
    
            # Render confirmation template
            handler.render_template(
                'Action',
                {
                    'confirmation': self.format_string % variables,
                    'action': self.action,
                    'post_variables': variables,
                }
            )
        return wrapper  

def confirmed_post(post_method):
    """
    Request decorator
        Verifies that the user is a member of this app
        Validates 'get' parameter 'p'
        Runs the post method (modifies the datastore)
        Redirects to /
    """
    def wrapper(handler):
        user = handler.get_valid_user()
        if not user:
            return handler.home()
        
        variables = handler.get_post_dict()
        """
        Run post method
        Params:
            user: current Google user
            variables: dict of get variables
        """
        post_method(handler, user, variables)
            
        # TODO: Add in post data to acknowledge delete
        return handler.home()
        
    return wrapper

class AddDomainAction(AuthenticatedRequest):
    """
    Delete a domain from a Pseudonym
    """
    @confirm_get('adddomain', "add the domain '%(domain)s' to the Pseudonym '%(mask)s'")
    def get(self, user, variables):
        pass

    @confirmed_post
    def post(self, user, variables):
        if 'mask' not in variables or 'domain' not in variables:
            return self.home()

        # Pseudonym in db?    
        pseudo = model.get(
            model.Pseudonym,
            mask=variables['mask'].lower(),
            user=user
        )
        if not pseudo:
            return self.home()
        
        domain = variables['domain'].lower()
        if domain not in pseudo.domains:
            pseudo.domains.append(domain)
            pseudo.put()
            
            logging.info("WEB: %s added '%s' to mask '%s'" % (
                user.email(),
                domain,
                pseudo.mask
            ))

class RemoveDomainAction(AuthenticatedRequest):
    """
    Delete a domain from a Pseudonym
    """
    @confirm_get('removedomain', "remove the domain '%(domain)s' from the Pseudonym '%(mask)s'")
    def get(self, user, variables):
        pass
        
    @confirmed_post
    def post(self, user, variables):
        if 'mask' not in variables or 'domain' not in variables:
            return self.home()
        
        # Pseudonym in db?    
        pseudo = model.get(
            model.Pseudonym,
            mask=variables['mask'].lower(),
            user=user
        )
        if not pseudo:
            return self.home()
            
        domain = variables['domain'].lower()
        if domain in pseudo.domains and len(pseudo.domains) > 1:
            pseudo.domains.remove(domain)
            pseudo.put()
            
            logging.info("WEB: %s removed '%s' from mask '%s'" % (
                user.email(),
                domain,
                pseudo.mask
            ))
        
class GenerateAction(AuthenticatedRequest):
    """
    Create a new Pseudonym action
    """
    @confirm_get('generate', "create a new Pseudonym with domain '%(domain)s'")
    def get(self, user, variables):
        pass
    
    @confirmed_post
    def post(self, user, variables):
        if 'domain' not in variables:
            return self.home()
        if variables['domain'] == '':
            return self.home()
            
        # Perform action
        pseudo = model.Pseudonym(
            user=user,
            domains=[variables['domain'].lower()],
        )
        pseudo.put()
        
        logging.info("WEB: %s generated mask '%s' with domain '%s'" % (
            user.email(),
            pseudo.mask,
            variables['domain']
        ))

class DeleteAction(AuthenticatedRequest):
    """
    Delete a Pseudonym action
    """
    @confirm_get('delete', "delete the Pseudonym '%(mask)s'")
    def get(self, user, variables):
        pass
        
    @confirmed_post
    def post(self, user, variables):
        if 'mask' not in variables:
            return self.home()
        
        # Pseudonym in db?    
        pseudo = model.get(
            model.Pseudonym,
            mask=variables['mask'].lower(),
            user=user
        )
        if not pseudo:
            return self.home()
        
        # Perform action
        if hasattr(pseudo, 'contact'):
            for contact in pseudo.contacts:
                contact.delete()
                
        logging.info("WEB: %s deleted mask '%s'" % (
            user.email(),
            pseudo.mask
        ))        
                
        pseudo.delete()
        
class DropAction(AuthenticatedRequest):
    """
    Toggle a Pseudonym's should_drop attribute
    """
    @confirm_get('drop', "change spam email discarding for the Pseudonym '%(mask)s'")
    def get(self, user, variables):
        pass
          
    @confirmed_post
    def post(self, user, variables):        
        if 'mask' not in variables:
            return self.home()
        
        # Pseudonym in db?    
        pseudo = model.get(
            model.Pseudonym,
            mask=variables['mask'].lower(),
            user=user
        )
        if not pseudo:
            return self.home()
        
        # Perform action
        pseudo.should_drop = not pseudo.should_drop
        pseudo.put()
        
        logging.info("WEB: %s set drop to '%r' for mask '%s'" % (
            user.email(),
            pseudo.should_drop,
            pseudo.mask
        ))