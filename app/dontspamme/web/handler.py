import logging

from google.appengine.ext.webapp.util import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from dontspamme.web.page import MainPage, AdminPage
from dontspamme.web.action import GenerateAction, DeleteAction, DropAction, AddDomainAction, RemoveDomainAction

application = webapp.WSGIApplication(
    [
        # Pages
        ('/', MainPage),
        ('/admin/?', AdminPage),
        
        # Actions
        ('/adddomain.*', AddDomainAction),
        ('/removedomain.*', RemoveDomainAction),
        ('/generate.*', GenerateAction),
        ('/delete.*', DeleteAction),
        ('/drop.*', DropAction),
        
        # Catch all
        ('/.*', webapp.RedirectHandler.new_factory('/'))
    ],
    debug=True
)

def main():
    logging.getLogger().setLevel(logging.DEBUG)
    run_wsgi_app(application)

if __name__ == "__main__":
    main()