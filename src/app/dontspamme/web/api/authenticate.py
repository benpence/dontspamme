from google.appengine.ext import webapp

import dontspamme.model as model
from dontspamme.web.api.handler import APIHandler
from dontspamme.web.authenticate import AuthenticatedRequest

class AuthenticationHandler(webapp.RequestHandler):
    """
    Simply tells a client whether they're logged in, a member, or neither
    """
    def read(self):
        user = users.get_current_user()
        
        if not user:
            output = '<<OUTPUT_NONE>>'
            
        elif model.get(model.Member, user=user):
            output = '<<OUTPUT_MEMBER>>'
        else:
            output = '<<OUTPUT_USER>>'

        self.writeout({'status': output})

application = webapp.WSGIApplication(
    [('/api/', handler.AuthenticationHandler)],
    debug=True
)

def main():
    logging.getLogger().setLevel(logging.DEBUG)
    run_wsgi_app(application)

if __name__ == "__main__":
    main()        