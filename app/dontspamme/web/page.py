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
        user = self.get_valid_user()
        if not user:
            return

        # User's pseudonyms newest->oldest
        pseudos = model.Pseudonym.all().filter('user =', user).order('-created')

        # TODO: Modify the template for the 11.7 functionality
        # TODO: Introduce key obfuscation in URL to deter cross site forgery
        #   Maybe get requests will ask for confirmation and post will not?
        self.render_template(
            'MainPage',
            {
                'pseudos': pseudos,
                'domain_name': dontspamme.config.domain_name,
            }
        )
        
class AdminPage(AuthenticatedRequest):
    # TODO: Write admin page
    pass    
    
