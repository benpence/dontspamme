import os

import dontspamme.model as model
from dontspamme.web.authenticate import AuthenticatedRequest

class MainPage(Page):
    """
    The root page that
        Displays the user's Pseudonyms
        Allows the user to toggle a Pseudonym's should_drop attribute
        Allows the user to generate new Pseudonyms
    """
    def get(self):
        user = self.app_user()

        # User's pseudonyms newest->oldest
        q = model.Pseudonym.all().filter('user =', user).order('-created')
        pseudos = q.all()

        template_values = {
            'pseudos': pseudos,
        }

        # TODO: Modify the template for the 11.7 functionality
        # TODO: Introduce key obfuscation in URL to deter cross site forgery
        #   Maybe get requests will ask for confirmation and post will not?
        self.render_template(
            'MainPage',
            template_values
        )
        
class AdminPage(Page):
    # TODO: Write admin page
    pass    
    
