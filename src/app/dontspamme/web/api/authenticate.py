"""
Tell client if they're (1) logged in and/or (2) a valid user
"""

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
        
		# Not logged in to Google
        if not user:
            output = '<<OUTPUT_NONE>>'
           
		# Not a member of this app
        elif model.get(model.Member, user=user):
            output = '<<OUTPUT_MEMBER>>'

		# All good
        else:
            output = '<<OUTPUT_USER>>'

		# Tell client
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