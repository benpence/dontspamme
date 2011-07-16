import logging

from google.appengine.ext import webapp 
from google.appengine.ext.webapp.mail_handlers import InboundMailHandler 
from google.appengine.ext.webapp.util import run_wsgi_app

import dontspamme.model as model
import dontspamme.util as util

from dontspamme.mail import from_stranger
from dontspamme.mail import from_user

class EmailHandler(InboundMailHandler):
    """
    Calls 'receive' method when an email is sent to STRING@APP_NAME.appspotmail.com

    Reference: http://code.google.com/appengine/docs/python/mail/
    """
    def receive(self, message):
        """
        Called when message an email message is received.

        Args:
            message: InboundEmailMessage
        """
        
        
        # To a pseudonym we know?
        to_address = util.EmailAddress(message.to)
        pseudo = model.get(model.Pseudonym, mask=to_address.user.lower())

        # Not stranger or reply?
        if not pseudo:
            logging.info("MAIL: No such pseudonym")
            return
        
        sender_address = util.EmailAddress(message.sender)
        
        # No contact in to address?
        if not to_address.contact:
            # Not user emailing their own pseudonym
            # TODO: Maybe we should change the response?
            if pseudo.user.email().lower() == sender_address.email.lower():
                logging.info("MAIL: User emailed themself")
                return
                
            from_stranger.handle(
                message,
                pseudo,
                util.EmailAddress(message.sender)
            )
            return

        # A reply to a contact, from the user's REAL email?
        if pseudo.user.email() == sender_address.email:
            from_user.handle(message, pseudo, to_address)
            return

        # Not from correct user...
        logging.info("MAIL: Invalid sender '%s' for reply to '%s+%s'" % (
            message.sender,
            pseudo.mask,
            to_address.contact
        ))

def main():
    logging.getLogger().setLevel(logging.DEBUG)
    application = webapp.WSGIApplication([EmailHandler.mapping()], debug=True)
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
