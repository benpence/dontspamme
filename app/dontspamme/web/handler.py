from google.appengine.ext import webapp

from dontspamme.web.page import MainPage, AdminPage
from dontspamme.web.action import GenerateAction, DeleteAction, DropAction

application = webapp.WSGIApplication(
    [
        ('/', MainPage),
        ('/admin', AdminPage)
        
        ('/generate.+', GenerateAction),
        ('/delete.+', DeleteAction),
        ('/drop.+', DropAction),
    ],
    debug=True
)

def main():
    logging.getLogger().setLevel(logging.DEBUG)
    webapp.util.run_wsgi_app(application)

if __name__ == "__main__":
    main()
