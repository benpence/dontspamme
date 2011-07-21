import logging
import json

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users

import dontspamme.model as model

class AuthenticationHandler(webapp.RequestHandler):
    """
    Simply tells a client whether they're logged in, a member, or neither
    """
    def get(self):
        user = users.get_current_user()
        
        if not user:
            output = '<<OUTPUT_NONE>>'
            
        elif model.get(model.Member, user=user):
            output = '<<OUTPUT_MEMBER>>'
        else:
            output = '<<OUTPUT_USER>>'

        self.response.out.write(
            json.dumps(
                {'status': output}
            )
        ) 

application = webapp.WSGIApplication(
    [('/api/', AuthenticationHandler)],
    debug=True
)

def main():
    logging.getLogger().setLevel(logging.DEBUG)
    run_wsgi_app(application)

if __name__ == "__main__":
    main()        