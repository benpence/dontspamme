from google.appengine.ext.webapp.mail_handlers import InboundMailHandler 

from google.appengine.ext import webapp 
from google.appengine.ext.webapp.util import run_wsgi_app

from model import Pseudonym
import common
import config

class EmailHandler(InboundMailHandler):
    def receive(self, message):
        pseudo = Pseudonym.search_by_to(mail_message.get('to'))
        tag = self.get_tag(message.get('to'))
        
        # To no one important
        if not pseudo:
            """DISCARD MESSAGE"""
        
        # Sent from user?
        if tag:
            # Response from owner
            if message.get('from') is psuedo.owner:
                address = Address.search_by_tag(tag)
                
                # Invalid tag
                if not address:
                    """DISCARD MESSAGE"""
                
                # Send message
                self.send_message(to=address.email, from=pseudo.mask, message)
                
            # Sender not owner
            else:
                """DISCARD MESSAGE"""
            
        # Sent from stranger
        else:
            address = Address(
                pseudo=pseudo,
                email=message.get('from'))
            
            domain = self.get_domain(message.get('from'))
            
            # Send response
            self.send_message(
                    message,
                    to=pseudo.owner,
                    from=pseudo+config.domain_name,
                    valid=domain in pseudo.domain or pseudo.domain in domain)
                
    def get_tag(self, to):
        start = '@'
        
    def get_domain(self, to):
        pass

    def send_message(self, recipient, owner):
        pass
        
        
application = webapp.WSGIApplication([EmailHandler.mapping()], debug=True)