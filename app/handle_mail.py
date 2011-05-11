import logging

from google.appengine.ext import webapp 
from google.appengine.ext.webapp.mail_handlers import InboundMailHandler # Receive

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
        to = util.EmailAddress(message.to)
        pseudo = model.get(model.Pseudonym, mask=to.user)

        if pseudo:
            self.from_stranger(message, pseudo)
            return

        # A reply to a contact?
        pseudo = model.get(model.Contact, email=sender)

        if to.contact and pseudo:
            self.from_user(message, pseudo, )

        # To non-existent user -> do not relay

    def from_stranger(self, message, pseudo):
        """
        Stranger emailing a pseudonym
        New strangers will be added as Contact.
        Strangers sending from invalid domain will be flagged.

        Args:
            message: dictionary message
            pseudo: Pseudonym of user
        """
        contact = model.get(model.Contact, pseudonym=pseudo, email=message.sender)

        # Create entry if new
        if not contact:
            contact = model.Contact(
                pseudonym=pseudo,
                email=message.sender,
                mask=util.generate_random_string()
            )
            contact.put()

            logging.info("New Contact")

        logging.info("Contact: %s -> %s" % (
            message.sender,
            message.to,
        ))

        # TODO: Add in flagging of spam
        #from_address = EmailAddress(message.sender)

        # Send response
        self.prepare_message(message)
        message.to = pseudo.user.email()
        #message_sender = 
        message.sender = "<%s+%s@%s>" % (
            pseudo.mask,
            contact.mask,
            config.domain_name
        )

        # TODO: Clear rest of fields to avoid exposing username on cc, bcc?
        message.send()

    def from_user(self, message, pseudo, to_address):
        """
        Send reply to contact.
        Sanitize message, verify contact contact mask, send email to contact.
        
        Args:
            message: dictionary message
            pseudo: Pseudonym of user
            to_address: recipient
        """
        contact = model.get(model.Contact, pseudonym=pseudo, mask=to_address.contact)
        
        # Invalid contact mask
        if not contact:
            # TODO: Should we warn user that they have sent invalid contact mask?
            logging.info("Invalid Reply: %s@%s -> ?" % (
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
