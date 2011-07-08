import os
import cgi

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.api import users

import dontspamme.config
import dontspamme.model as model

class AuthenticatedRequest(webapp.RequestHandler):
    """
    Authenticates users of the app.
    Includes some helper functions for handling requests.
    """
    TEMPLATE_DIRECTORY = os.path.join(
        os.path.dirname(__file__),
        'templates'
    )
    
    def home(self):
        self.redirect('/')
        return False
    
    def get_valid_user(self):
        user = model.get(
            model.User,
            user=users.get_current_user()
        )

        if not user:
            referral = dontspamme.config.referral_for_non_users
            if 'http' not in referral:
                referral = 'http://' + referral
                
            self.redirect(referral)
            return
        
        return user.user

    def get_post_dict(self):
        return dict((
            (key, cgi.escape(self.request.get(key)))
            for key in self.request.arguments()
        ))

    def render_template(self, template_name, template_values):
        self.response.out.write(
            template.render(
                os.path.join(
                    self.TEMPLATE_DIRECTORY,
                    template_name + '.html',
                ),
                template_values
            )
        )