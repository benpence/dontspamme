import os

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from google.appengine.api import users

import util
import model

class MainPage(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        
        if not user:
            self.redirect(users.create_login_url(self.request.uri))
'
        # User's pseudonyms newest->oldest
        q = model.Pseudonym.all().filter('user =', user).order('-created')
        pseudos = q.all()

        template_values = {
            'pseudos': pseudos,
        }

        path = os.path.join(
            os.path.dirname(__file__),
            'templates',
            'index.html'
        )

        self.response.out.write(template.render(path, template_values))

class Generate(webapp.RequestHandler):
    def post(self):
        user = users.get_current_user()
        
        if not user:
            self.redirect(users.create_login_url('/'))
        
        pseudo = Pseudonym(
            user=user,
            mask=util.generate_random_string()
        )
        pseudo.put()

        self.redirect('/')

application = webapp.WSGIApplication(
                                     [('/', MainPage),
                                      ('/generate', Generate)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
