import cgi

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

import common
from model import Pseudonym

class MainPage(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        
        if not user:
            self.redirect(users.create_login_url(self.request.uri))
        
        pseudonyms = db.GqlQuery("SELECT * FROM Pseudonym WHERE user = :user ORDER BY created ASC",
            user=user)
        
        self.response.out.write('<html><body>')
        for pseudo in pseudonyms:
            self.response.out.write(cgi.escape(pseudo.user.nickname() + ' ' + pseudo.mask + '@dontspam.me ' + pseudo.domain + ' ' + str(pseudo.created)) + "<br>")
        
        # Write the submission form and the footer of the page
        self.response.out.write("""
              <form action="/generate" method="post">
                <div><textarea name="domain" rows="1" cols="20"></textarea></div>
                <div><input type="submit" value="Generate Pseudonym"></div>
              </form>
            </body>
          </html>""")

class Generate(webapp.RequestHandler):
    def post(self):
        user = users.get_current_user()
        
        if not user:
            self.redirect(users.create_login_url('/'))
        
        pseudo = Pseudonym()
        pseudo.user = user
        pseudo.mask = common.random_hash()
        pseudo.domain = self.request.get('domain')

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