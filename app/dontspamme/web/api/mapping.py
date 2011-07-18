import logging

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

import dontspamme.web.api.handler as handler
    
application = webapp.WSGIApplication(
    [
        ('/api/member\?.*', handler.MemberHandler),
        ('/api/member/?', handler.MemberHandler),
        ('/api/member/(.+)/?', handler.MemberHandler),
        
        ('/api/pseudonym\?.*', handler.PseudonymHandler),
        ('/api/pseudonym/?', handler.PseudonymHandler),
        ('/api/pseudonym/(.+)/?', handler.PseudonymHandler),
        
        ('/api/domain/(.+)/?', handler.DomainHandler),
    ],
    debug=True
)

def main():
    logging.getLogger().setLevel(logging.DEBUG)
    run_wsgi_app(application)

if __name__ == "__main__":
    main()