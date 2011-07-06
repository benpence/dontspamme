import logging

from google.appengine.ext import webapp 
from google.appengine.ext.webapp.mail_handlers import InboundMailHandler # Receive

import dontspamme.model as model
import dontspamme.util as util

from dontspamme.mail.from_user import from_user
from dontspamme.mail.from_stranger import from_stranger

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
        logging.debug("Received Mail: \n" + message.original)

        # To a pseudonym we know?
        to_address = util.EmailAddress(message.to)
        pseudo = model.get(model.Pseudonym, mask=to_address.user)

        if pseudo:
            from_stranger(message, pseudo, to_address.email)
            return

        # A reply to a contact from a user's REAL email?
        # TODO: Find an efficient way to match real email to datastore (add Pseudonym field?)
        pseudo = util.first(
            model.Pseudonym.all(),
            lambda p: p.email in message.sender
        )

        if to_address.contact and pseudo:
            from_user(message, pseudo, to_address)

        # To non-existent user -> do not relay

def main():
    logging.getLogger().setLevel(logging.DEBUG)
    application = webapp.WSGIApplication([EmailHandler.mapping()], debug=True)
    webapp.util.run_wsgi_app(application)

if __name__ == '__main__':
    main()
