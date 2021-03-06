import os
import cgi
import logging
import re

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.api import users

import dontspamme.config
import dontspamme.util as util
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
    
    HOME = '/'
    EXIT = util.prepend_if_absent(
        'http://',
        dontspamme.config.referral_for_non_users
    )
    
    def get_valid_member(self):
        current_user = users.get_current_user()
        
        valid_user = model.get(
            model.Member,
            user=current_user
        )
        
        member = valid_user or self.create_admin_if_needed(current_user)

        if not member:
            user_regex = re.compile(re.escape(current_user.email()), re.IGNORECASE)
            user_len = len(current_user.email())
            
            for m in model.Member.all():
                # TODO: Look into how this might open a security hole (if it smells like a pig and tastes like a pig, it might be bacon)
                # Update user references to actual user reference
                if user_regex.match(m.user.email()) and len(m.user.email()) == user_len:
                    m.user = current_user
                    m.put()
                    member = m
                    break
        
            if not member:
                self.redirect(self.EXIT)
                return
        
        return member

    def get_admin_member(self):
        current_user = users.get_current_user()
        
        member = self.create_admin_if_needed(current_user)
        if not member:
            self.redirect(self.EXIT)
        
        return member

    def create_admin_if_needed(self, user):
        if users.is_current_user_admin():
            member = model.get(
                model.Member,
                user=user
            )
            
            if not member:
                member = model.Member(user=user)
                member.put()
            
            return member

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