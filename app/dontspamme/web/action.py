import cgi

import dontspamme.util as util
import dontspamme.model as model
from dontspamme.web.authenticate import AuthenticatedRequest

class GenerateAction(AuthenticatedRequest):
    """
    Create a new Pseudonym action
    """
    def get(self):
        user = self.app_user()
        
        # Properly formatted request?
        domain_str = cgi.escape(self.request.post('domain'))
        if not domain_str:
            self.redirect('/')
        
        self.render_template(
            'Action',
            {
                'confirmation': "create a new Pseudonym with domain '%s'" % domain_str,
                'action': 'generate',
                'post_variables': self.request.getall(),
            }
        )
    
    def post(self):
        # TODO: Add logging for generate
        user = self.app_user()
        
        # TODO: ? Does self.request.get work in post?
        domain_str = cgi.escape(self.request.post('domain'))
        
        # Perform action
        pseudo = Pseudonym(
            user=user,
            mask=util.generate_random_string(),
            domains=[domain_str],
            should_drop=False
        )
        pseudo.put()

        # TODO: Add in post data to acknowledge generate
        self.redirect('/')

class DeleteAction(AuthenticatedRequest):
    """
    Delete a Pseudonym action
    """
    def get(self):
        user = self.app_user()
        
        # Properly formed request?
        pseudo_str = cgi.escape(self.request.get('pseudonym'))
        if not pseudo_str:
            self.redirect('/')
        
        self.render_template(
            'Action',
            {
                'confirmation': "delete the Pseudonym '%s'" % pseudo_str,
                'action': 'delete',
                'post_variables': self.request.getall()
            }
        )
        
    def post(self):
        # TODO: Add logging for delete
        user = self.app_user()
        
        # Properly formed request?
        pseudo_str = cgi.escape(self.request.post('pseudonym'))
        if not pseudo_str:
            self.redirect('/')
        
        # Pseudonym in db?    
        pseudo = model.get(
            model.Pseudonym,
            mask=pseudo_str,
            user=user
        )
        if not pseudo:
            self.redirect('/')
        
        # Perform action
        # TODO: Implement the deletion
        # for contact in pseudo.contacts:
        #   contact.drop()
        # pseudo.drop()
        
        # TODO: Add in post data to acknowledge delete
        self.redirect('/')

class DropAction(AuthenticatedRequest):
    """
    Toggle a Pseudonym's should_drop attribute
    """
    def get(self):
        user = self.app_user()
        
        # Properly formed request?
        pseudo_str = cgi.escape(self.request.get('pseudonym'))
        if not pseudo_str:
            self.redirect('/')
            
        confirm_str = ['start', 'stop'][pseudo.should_drop] + " discarding spam emails to the Pseudonym '%s'" % pseudo.mask
        
        self.render_template(
            'Action',
            {
                'confirmation': confirm_str,
                'action': 'drop',
                'post_variables': self.request.getall()
            }
        )
        
    def post(self):
        # TODO: Add logging for drop
        user = self.app_user()
        
        # Properly formed request?
        pseudo_str = cgi.escape(self.request.post('pseudonym'))
        if not pseudo_str:
            self.redirect('/')
        
        # Pseudonym in db?    
        pseudo = model.get(
            model.Pseudonym,
            mask=pseudo_str,
            user=user
        )
        if not pseudo:
            self.redirect('/')
        
        # Perform action
        pseudo.should_drop = not pseudo.should_drop
        
        # TODO: Add in post data to acknowledge drop
        self.redirect('/')