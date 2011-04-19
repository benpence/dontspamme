from google.appengine.ext.webapp.mail_handlers import InboundMailHandler 

from google.appengine.ext import webapp 
from google.appengine.ext.webapp.util import run_wsgi_app

import model
import ext

class EmailHandler(InboundMailHandler):
    """
    Calls 'receive' method when an email is sent to STRING@APP_NAME.appspot.com
    """
    
    def receive(self, message):
        """
        Interace 

        """
        sender = message.get('from')
        receiver = message.get('to')

        # Email from somebody?
        pseudo = ext.where(model.Pseudonym, 1, email=receiver)

        if pseudo:
            self.fromStranger(pseudo, sender, message)
        

        # Reply from user?
        tag = self.getTag(receiver)
        pseudo = ext.where(model.Pseudonym, 1, email=sender)

        if tag and pseudo:
            self.fromUser(pseudo, tag, message)

        # To non-existent user -> do not relay

    def fromStranger(self, pseudo, sender, message):
        """
        Stranger emailing a pseudonym
        New strangers will be added as Contact.
        Strangers sending from invalid domain will be flagged.

        Args:
            pseudo: Pseudonym of user
            sender: stranger email address
            message: dictionary message
        """

        tag = ext.where(
            model.Contact
            1,
            email=sender
        )

        # Create entry if new
        if not tag:
            tag = model.Contact(
                psuedo=pseudo,
                """TODO: Write method to generate tags"""
                email=sender,
            )


        domain = self.getDomain(sender)

        # Send response
        self.send(
            """TODO: Write all cool stuff into message body-header for marking-as-spam etc"""
            message,
            pseudo.user.email(),
            """TODO: Write function to insert tag into reply-to address"""
            pseudo.mask+config.domain_name,
        )

    def fromUser(self, pseudo, tag, message):
        """
        Send reply to contact.
        Sanitize message, verify contact tag, send email to contact.
        
        Args:
            pseudo: Pseudonym of user
            sender: stranger email address
            message: dictionary message
        """
        contact = ext.where(model.Contact, 1, tag=tag)
        
        # Invalid tag
        if not contact:
            """TODO: Should we warn user that they have sent invalid tag?"""
            return
        
        # Send message
        self.send(
            self.sanitize(message),
            contact.email,
            pseudo.mask+config.domain_name,
        )
                
    def sanitizeMessage(self, message):
        """
        Remove all traces of User's REAL email address from message body.
        """

        """TODO: Write sanitization"""
        
        return message

    def send(self, message, receiver, sender):
        """
        Send an email
        """

        """TODO: Implement sending of email..."""

        if not (message and receiver and sender):
            raise exception.InputError()
                
    def getTag(self, email):
        return ext.email_split(email, '+', '@')
        
    def getDomain(self, email):
        return ext.email_split(email, '@')
        
application = webapp.WSGIApplication([EmailHandler.mapping()], debug=True)
