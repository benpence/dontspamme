import logging

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from dontspamme.web.page import MainPage, AdminPage
from dontspamme.web.action import AddPseudonymAction, DeletePseudonymAction, DropPseudonymAction, AddDomainAction, DeleteDomainAction, AddUserAction, DeleteUserAction

application = webapp.WSGIApplication(
    [
        # Pages
        ('/', MainPage),
        ('/admin/?', AdminPage),
        
        # Actions
        ('/adddomain.*', AddDomainAction),
        ('/deletedomain.*', DeleteDomainAction),
        
        ('/addpseudonym.*', AddPseudonymAction),
        ('/deletepseudonym.*', DeletePseudonymAction),
        ('/droppseudonym.*', DropPseudonymAction),
        
        ('/adduser.*', AddUserAction),
        ('/deleteuser.*', DeleteUserAction),
        
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