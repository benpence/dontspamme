from google.appengine.ext.webapp.mail_handlers import InboundMailHandler 

from google.appengine.ext import webapp 
from google.appengine.ext.webapp.util import run_wsgi_app

from model import Pseudonym
import common
import config

class EmailHandler(InboundMailHandler):
    """
    Calls 'receive' method when an email is sent to STRING@APP_NAME.appspot.com
    """
    
    def receive(self, message):
        pseudo = Pseudonym.search_by_to(mail_message.get('to'))
        tag = self.get_tag(message.get('to'))
        
        # To no one important
        if not pseudo:
            """DISCARD MESSAGE"""
        
        # Sent from user
        if tag:
            self.from_owner(message, pseudo, tag)
            
        # Sent from somebody else
        else:
            self.to_owner(message, pseudo)
                     
    def from_owner(self, message, pseudo, tag):
        """
        message:{str:...} | pseudo:Pseudonym | tag:str -> None
        
        Tag specified; response from owner
        """
        
        # Sender not owner
        if message.get('from') is not psuedo.owner:
            """DISCARD MESSAGE"""
            
        address = Address.search_by_tag(tag)
        
        # Invalid tag
        if not address:
            """DISCARD MESSAGE"""
        
        # Send message
        self.send(
            message=message,
            to=address.email,
            from=pseudo.mask)

    def to_owner(self, message, pseudo):
        """
        message:{str:...} | pseudo:Pseudonym -> None
        
        No tag specified; email to owner
        """

        # Will create entry if necessary
        tag = Address.email_to_tag(
            pseudo.owner,
            message.get('from'))

        domain = self.get_domain(message.get('from'))

        # Send response
        self.send(
            message=self.sanitize_message(
                message
                valid=domain in pseudo.domain or pseudo.domain in domain),
            to=pseudo.owner,
            from=pseudo.mask+config.domain_name)
                
    def sanitize_message(self, message, valid=True):
        """
        message:{str:...} | valid:bool -> {str:str}
        """
        
        return message

    def send(self, message=None, to=None, from=None):
        """
        message:{str:...} | to:str | from:str -> None
        """

        # Logging
        if not (message and to and from):
            """LOG"""
                
    def get_tag(self, to):
        return common.email_split(to, start='+', end='@')
        
    def get_domain(self, to):
        return common.email_split(to, start='@')
        
application = webapp.WSGIApplication([EmailHandler.mapping()], debug=True)