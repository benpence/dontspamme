import logging

from google.appengine.ext import webapp 
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp.mail_handlers import InboundMailHandler # Receive
from google.appengine.api import mail # Send

class EmailHandler(InboundMailHandler):
    """
    Calls 'receive' method when an email is sent to STRING@APP_NAME.appspot.com

    Tutorial: http://code.google.com/appengine/docs/python/mail/
    """
    
    def receive(self, message):
        """
        Main API function. Called when message received.
        """

        logging.debug(message.original)

        mail.send_mail(
            sender="ben@bmpence.appspotmail.com",
            to="bmpence@gmail.com",
            subject="Test subject",
            body='\n==\n'.join((
                message.sender,
                message.to,
                #message.cc,
                #message.bcc,
                #message.reply_to,
                message.subject,
                str(message.body)
            ))
        )

def main():
    logging.getLogger().setLevel(logging.DEBUG)
    application = webapp.WSGIApplication([EmailHandler.mapping()], debug=True)
    webapp.util.run_wsgi_app(application)

if __name__ == '__main__':
    main()
