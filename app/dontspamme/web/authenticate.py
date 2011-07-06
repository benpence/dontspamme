from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users
from google.appengine.ext.webapp import template

import dontspamme.config
import dontspamme.model as model

class AuthenticatedRequest(webapp.RequestHandler):
    TEMPLATE DIRECTORY = os.path.join(
        os.path.dirname(__file__),
        'templates'
    )
    
    def app_user(self):
        user = model.get(
            model.User,
            user=users.get_current_user()
        )
        
        if not user:
            self.redirect(dontspamme.config.referral_for_non_users)
        
        return user.user


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