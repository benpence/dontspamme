import logging

from google.appengine.ext import webapp 
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp.mail_handlers import InboundMailHandler # Receive
from google.appengine.api import mail # Send

import model
import config

class EmailHandler(InboundMailHandler):
    """
    Calls 'receive' method when an email is sent to STRING@APP_NAME.appspot.com

    Tutorial: http://code.google.com/appengine/docs/python/mail/
    """
    
    def receive(self, message):
        """
        Main API function. Called when message received.
        """

        sender = message.sender
        to = message.to

        # Email from somebody?
        pseudo = model.where(model.Pseudonym, 1, email=to)

        if pseudo:
            self.from_stranger(pseudo, sender, message)
        

        # Reply from user?
        tag = self.email_split(to, '+', '@')
        pseudo = model.where(model.Pseudonym, 1, email=sender)

        if tag and pseudo:
            self.from_user(pseudo, tag, message)

        # To non-existent user -> do not relay

    def from_stranger(self, pseudo, sender, message):
        """
        Stranger emailing a pseudonym
        New strangers will be added as Contact.
        Strangers sending from invalid domain will be flagged.

        Args:
            pseudo: Pseudonym of user
            sender: stranger email address
            message: dictionary message
        """

        tag = model.where(
            model.Contact,
            1,
            email=sender
        )

        # Create entry if new
        if not tag:
            tag = model.Contact(
                psuedo=pseudo,
                # TODO: Write method to generate tags
                email=sender
            )

        domain = self.email_split(sender, '@')

        # Send response
        self.prepare_message(message)
        message.to = pseudo.user.email()
        # TODO: Write function to insert tag into reply-to address
        message.reply_to = pseudo.mask+config.domain_name

        message.send()

    def from_user(self, pseudo, tag, message):
        """
        Send reply to contact.
        Sanitize message, verify contact tag, send email to contact.
        
        Args:
            pseudo: Pseudonym of user
            sender: stranger email address
            message: dictionary message
        """
        contact = model.where(model.Contact, 1, tag=tag)
        
        # Invalid tag
        if not contact:
            # TODO: Should we warn user that they have sent invalid tag?
            return
        
        # Send message
        self.sanitize(message, pseudo.user.email())
        message.sender = pseudo.mask + config.domain_name
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

    def email_split(email, start='', end=''):
        """
        Returns rightmost string that is contained by start and end.
        """
        partition = email[email.rfind(start): email.rfind(end)]

        if not partition:
            return None

        return partition[1:]

def main():
    logging.getLogger().setLevel(logging.DEBUG)
    application = webapp.WSGIApplication([EmailHandler.mapping()], debug=True)
    webapp.util.run_wsgi_app(application)

if __name__ == '__main__':
    main()
