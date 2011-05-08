import logging

from google.appengine.ext import webapp 
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp.mail_handlers import InboundMailHandler # Receive
from google.appengine.api import mail # Send

import model
import config
import util

class EmailHandler(InboundMailHandler):
    """
    Calls 'receive' method when an email is sent to STRING@APP_NAME.appspotmail.com

    Tutorial: http://code.google.com/appengine/docs/python/mail/
    """
    def receive(self, message):
        """
        Called when message an email message is received.
        """
        logging.debug("Received Mail: \n" + message.original)

        # To a pseudonym we know?
        mask = util.string_between(message.to, end="@")
        pseudo = model.get(model.Pseudonym, mask=mask)

        if pseudo:
            self.from_stranger(pseudo, message)

        # A reply to a contact?
        contact_mask = self.string_between(message.to, '+', '@')
        pseudo = model.get(model.Pseudonym, email=sender)

        if contact_mask and pseudo:
            self.from_user(pseudo, contact_mask, message)

        # To non-existent user -> do not relay

    def from_stranger(self, pseudo, message):
        """
        Stranger emailing a pseudonym
        New strangers will be added as Contact.
        Strangers sending from invalid domain will be flagged.

        Args:
            pseudo: Pseudonym of user
            message: dictionary message
        """

        contact = model.get(model.Contact, email=message.sender)

        # Create entry if new
        if not contact:
            contact_mask = model.Contact(
                psuedo=pseudo,
                # TODO: Write method to generate contact masks
                email=message.sender
            )
            logging.info("INVALID Stranger: %s -> %s" % (
                message.sender,
                message.to,
            ))

        logging.info("Stranger: %s -> %s" % (
            message.sender,
            message.to,
        ))

        domain = self.string_between(message.sender, '@')

        # Send response
        self.prepare_message(message)
        message.to = pseudo.user.email()
        # TODO: Write function to insert contact mask into reply-to address
        message.reply_to = pseudo.mask + '@' + config.domain_name

        message.send()

    def from_user(self, pseudo, contact_mask, message):
        """
        Send reply to contact.
        Sanitize message, verify contact contact mask, send email to contact.
        
        Args:
            pseudo: Pseudonym of user
            contact_mask: string between + and @
            message: dictionary message
        """
        contact = model.get(model.Contact, mask=contact_mask)
        
        # Invalid contact mask
        if not contact:
            # TODO: Should we warn user that they have sent invalid contact mask?
            logging.info("INVALID Reply: %s@%s -> ?" % (
                pseudo.mask, config.domain,
            ))
            return

        logging.info("Reply: %s@%s -> %s" % (
            pseudo.mask, config.domain,
            contact.email,
        ))
        
        # Send message
        self.sanitize(message, pseudo.user.email())
        message.sender = pseudo.mask + '@' + config.domain_name
        message.to = contact.email,

        message.send()
                
    def prepare_message(self, message):
        """
        Add header to message body.
        """
        # TODO: Implement preparation of message
        pass

    def sanitize_message(self, message, email):
        """
        Remove all traces of User's REAL email address from message body.
        """
        # TODO: Write sanitization
        pass

def main():
    logging.getLogger().setLevel(logging.DEBUG)
    application = webapp.WSGIApplication([EmailHandler.mapping()], debug=True)
    webapp.util.run_wsgi_app(application)

if __name__ == '__main__':
    main()
