import logging

from google.appengine.api.users import User

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
            member = handler.get_valid_member()
            if not member:
                return handler.HOME
            
            variables = handler.get_post_dict()
            """
            Run get method
            Allow get method to 'break out' of response by returning False
            Params:
                member: current Google user
                variables: dict of get variables
            """
            redirect = get_method(handler, member, variables)
            if redirect:
                return handler.redirect(redirect)
    
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
        member = handler.get_valid_member()
        if not member:
            return handler.HOME
        
        variables = handler.get_post_dict()
        """
        Run post method
        Params:
            member: current Google user
            variables: dict of get variables
        """
        redirect = post_method(handler, member, variables)
        if redirect:
            return handler.redirect(redirect)
            
        # TODO: Add in post data to acknowledge delete
        return handler.redirect(handler.HOME)
        
    return wrapper

class AddDomainAction(AuthenticatedRequest):
    """
    Delete a domain from a Pseudonym
    """
    @confirm_get('adddomain', "add the domain '%(domain)s' to the Pseudonym '%(mask)s'")
    def get(self, member, variables):
        pass

    @confirmed_post
    def post(self, member, variables):
        if 'mask' not in variables or 'domain' not in variables:
            return self.HOME

        # Pseudonym in db?    
        pseudo = model.get(
            model.Pseudonym, 1,
            mask=variables['mask'].lower(),
            member=member
        )
        if not pseudo:
            return self.HOME
        
        domain = variables['domain'].lower()
        if domain not in pseudo.domains:
            pseudo.domains.append(domain)
            pseudo.put()
            
            logging.info("WEB: %s added '%s' to mask '%s'" % (
                member.user.email(),
                domain,
                pseudo.mask
            ))

class DeleteDomainAction(AuthenticatedRequest):
    """
    Delete a domain from a Pseudonym
    """
    @confirm_get('removedomain', "remove the domain '%(domain)s' from the Pseudonym '%(mask)s'")
    def get(self, member, variables):
        pass
        
    @confirmed_post
    def post(self, member, variables):
        if 'mask' not in variables or 'domain' not in variables:
            return self.HOME
        
        # Pseudonym in db?    
        pseudo = model.get(
            model.Pseudonym, 1,
            mask=variables['mask'].lower(),
            member=member
        )
        if not pseudo:
            return self.HOME
            
        domain = variables['domain'].lower()
        if domain in pseudo.domains and len(pseudo.domains) > 1:
            pseudo.domains.remove(domain)
            pseudo.put()
            
            logging.info("WEB: %s removed '%s' from mask '%s'" % (
                member.user.email(),
                domain,
                pseudo.mask
            ))
        
class AddPseudonymAction(AuthenticatedRequest):
    """
    Create a new Pseudonym action
    """
    @confirm_get('addpseudonym', "create a new Pseudonym with domain '%(domain)s'")
    def get(self, member, variables):
        pass
    
    @confirmed_post
    def post(self, member, variables):
        if 'domain' not in variables:
            return self.HOME
        if variables['domain'] == '':
            return self.HOME
            
        # Perform action
        pseudo = model.Pseudonym(
            member=member,
            domains=[variables['domain'].lower()],
            mask=util.generate_random_string()
        )
        pseudo.put()
        
        logging.info("WEB: %s generated mask '%s' with domain '%s'" % (
            member.user.email(),
            pseudo.mask,
            variables['domain']
        ))

class DeletePseudonymAction(AuthenticatedRequest):
    """
    Delete a Pseudonym action
    """
    @confirm_get('deletepseudonym', "delete the Pseudonym '%(mask)s'")
    def get(self, member, variables):
        pass
        
    @confirmed_post
    def post(self, member, variables):
        if 'mask' not in variables:
            return self.HOME
        
        # Pseudonym in db?    
        pseudo = model.get(
            model.Pseudonym, 1,
            mask=variables['mask'].lower(),
            member=member
        )
        if not pseudo:
            return self.HOME
        
        # Perform action
        for contact in pseudo.contacts:
            contact.delete()
                
        logging.info("WEB: %s deleted mask '%s'" % (
            member.user.email(),
            pseudo.mask
        ))        
                
        pseudo.delete()
        
class DropPseudonymAction(AuthenticatedRequest):
    """
    Toggle a Pseudonym's should_drop attribute
    """
    @confirm_get('droppseudonym', "change spam email discarding for the Pseudonym '%(mask)s'")
    def get(self, member, variables):
        pass
          
    @confirmed_post
    def post(self, member, variables):        
        if 'mask' not in variables:
            return self.HOME
        
        # Pseudonym in db?    
        pseudo = model.get(
            model.Pseudonym, 1,
            mask=variables['mask'].lower(),
            member=member
        )
        if not pseudo:
            return self.HOME
        
        # Perform action
        pseudo.should_drop = not pseudo.should_drop
        pseudo.put()
        
        logging.info("WEB: %s set drop to '%r' for mask '%s'" % (
            member.user.email(),
            pseudo.should_drop,
            pseudo.mask
        ))

class AddUserAction(AuthenticatedRequest):
    @confirm_get('adduser', "add the user '%(email)s' to the users list")
    def get(self):
        pass
        
    @confirmed_post
    def post(self, member, variables):
        if 'email' not in variables:
            return '/admin'
        
        user = User(variables['email'].lower())
        
        # TODO: Add error checking for non-existent users    
        # User already in db?
        member = model.get(
            model.Member, 1,
            user=user
        )
        if member:
            return '/admin'
            
        # Perform add
        model.Member(user=user).put()
        
        logging.info("WEB: Added member '%s'" % variables['email'])
        
        return '/admin'
    
class DeleteUserAction(AuthenticatedRequest):
    @confirm_get('deleteuser', "delete the user '%(email)s from the users list")
    def get(self):
        pass
    
    @confirmed_post
    def post(self, member, variables):
        if 'email' not in variables:
            return '/admin'
            
        # TODO: Add error checking for non-existent users
        # User in db?
        member = model.get(
            model.Member, 1,
            user=User(variables['email'].lower())
        )
        if not member:
            return '/admin'
        
        # Perform deletion
        for pseudo in member.pseudonyms:
            for contact in pseudo.contacts:
                contact.delete()
            pseudo.delete()
        member.delete()
        
        logging.info("WEB: Deleted member '%s'" % variables['email'])
        
        return '/admin'