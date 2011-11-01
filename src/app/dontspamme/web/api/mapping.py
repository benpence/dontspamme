"""
URL Mapping for API calls
"""

import logging

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from dontspamme.web.api import handler
    
application = webapp.WSGIApplication(
    [
        # Member
        (r'/api/member/(.+)/?', handler.MemberHandler),
        (r'/api/member', handler.MemberHandler),        

        # Pseudonym
        (r'/api/pseudonym/(.+)/?', handler.PseudonymHandler),
        (r'/api/pseudonym', handler.PseudonymHandler),

        # Domain
        ('/api/domain/(.+)/?', handler.DomainHandler),
    ],
    debug=True
)

def main():
    logging.getLogger().setLevel(logging.DEBUG)
    run_wsgi_app(application)

if __name__ == "__main__":
    main()