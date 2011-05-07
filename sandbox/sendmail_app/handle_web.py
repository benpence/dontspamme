from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

class MainPage(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        
        if not user:
            self.redirect(users.create_login_url(self.request.uri))
        
        # Write the submission form and the footer of the page
        self.response.out.write("""
              <form action="/generate" method="post">
                <div><textarea name="domain" rows="1" cols="20"></textarea></div>
                <div><input type="submit" value="Generate Pseudonym"></div>
              </form>
            </body>
          </html>""")

application = webapp.WSGIApplication(
                                     [('/', MainPage)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
