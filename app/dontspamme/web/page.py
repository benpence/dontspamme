import logging

import dontspamme.config
import dontspamme.model as model
from dontspamme.web.authenticate import AuthenticatedRequest

class MainPage(AuthenticatedRequest):
    """
    The root page that
        Displays the user's Pseudonyms
        Allows the user to toggle a Pseudonym's should_drop attribute
        Allows the user to generate new Pseudonyms
    """
    def get(self):
        member = self.get_valid_member()
        if not member:
            return

        # User's pseudonyms newest->oldest
        pseudos = model.Pseudonym.all().filter('member =', member).order('-created')

        # TODO: Introduce key obfuscation in URL to deter cross site forgery
        #   Maybe get requests will ask for confirmation and post will not?
        self.render_template(
            'MainPage',
            {
                'pseudos': pseudos,
                'mail_domain': dontspamme.config.mail_domain,
            }
        )
        
class AdminPage(AuthenticatedRequest):
    """
    For /admin
        Displays the application's users (minus the admin)
        Allows the admin to add/drop users from the application
    """
    def get(self):
        member = self.get_admin_member()
        if not member:
            return
        
        self.render_template(
            'AdminPage',
            {
                'members': model.Member.all(),
                'admin': member
            }
        )