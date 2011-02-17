
from google.appengine.ext.webapp.mail_handlers import InboundMailHandler 

from google.appengine.ext import webapp 
from google.appengine.ext.webapp.util import run_wsgi_app

from model import Pseudonym

class EmailHandler(InboundMailHandler):
    def receive(self, mail_message):
        pseudonyms = Pseudonyms.all()
        
        for recipient in mail_message.to:
            owner = pseudonyms.filter("mask =", recipient)
            
            if owner:
                self.forward_email(recipient, owner)

    def forward_email(self, recipient, owner):
        

        
application = webapp.WSGIApplication([EmailHandler.mapping()], debug=True)