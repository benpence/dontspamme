import logging

from google.appengine.ext import webapp 
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp.mail_handlers import InboundMailHandler # Receive
from google.appengine.api import mail # Send

class EmailHandler(InboundMailHandler):
    """
    Calls 'receive' method when an email is sent to STRING@APP_NAME.appspotmail.com

    Tutorial: http://code.google.com/appengine/docs/python/mail/
    """
    
    def receive(self, message):
        """
        Main API function. Called when message received.
        """
        
        logging.debug("Recieved:\n" + str(message.original))
        message.sender = "fakeemailtest@durp.com <robots@bmpence.appspotmail.com>"
        message.reply_to = message.sender
        message.to = "nosnevelxela@gmail.com"        
        message.send()

application = webapp.WSGIApplication([EmailHandler.mapping()], debug=True)

def main():
    logging.getLogger().setLevel(logging.DEBUG)
    webapp.util.run_wsgi_app(application)

if __name__ == '__main__':
    main()
