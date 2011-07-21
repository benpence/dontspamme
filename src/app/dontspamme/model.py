from google.appengine.ext import db

import dontspamme.util as util
import dontspamme.config

class Member(db.Model):
    """
    A member associated with this app. Primary function is to disallow other
    users from using app.

    Attributes:
        user: Google user
    """
    user         = db.UserProperty()
    
    def __eq__(self, other):
        if isinstance(other, Member):
            return self.user == other.user
        return NotImplemented

    def __ne__(self, other):
        result = self.__eq__(other)
        if result is NotImplemented:
            return result
        return not result

class Pseudonym(db.Model):
    """
    A pseudonym (mask) for a user.

    Attributes:
        user: Owner of pseudonym
        mask: Pseudonym string. example: a38g70a
        domain/domains: Legitimate domain(s).
        contact/contacts: Collection of contacts associated with this pseudonym
        should_drop: boolean
            True  -> drop emails from invalid contacts
            False -> flag emails from invalid contacts
        created: datetime of creation time
    """
    member        = db.ReferenceProperty(Member, collection_name='pseudonyms')
    mask          = db.StringProperty(multiline=False)    

    domains       = db.StringListProperty()
    should_drop   = db.BooleanProperty(default=False)
    
    created       = db.DateTimeProperty(auto_now_add=True)

    @property
    def email(self):
        """
        Returns pseudonym's full local email address
        """
        return '%s@%s' % (self.mask, dontspamme.config.mail_domain)
            
class Contact(db.Model):
    """
    A mapping of a hashstring -> email address.
    Allows the user of the Pseudonym to indicate to whom they are responding.

    Attributes:
        pseudonym: Pseudonym object. Represents who this is a contact for.
        mask: str that maps to the email of the contact
        email: the email of the contact ex: steve@corp.microsoft.com
        name: the name string, if applicable, from the contact's first correspondence
    """
    # TODO: Allow user of Pseudonym to initiate an email conversation.
    # While this is not what the tool was intended for, it should be possible.

    pseudonym   = db.ReferenceProperty(Pseudonym, collection_name='contacts')
    mask        = db.StringProperty(multiline=False)
    
    email       = db.StringProperty(multiline=False)
    name        = db.StringProperty(multiline=False)
    
    created     = db.DateTimeProperty(auto_now_add=True)

def constrain(cls, **kwargs):
    q = cls.all()

    for key, value in kwargs.items():
        q.filter(key + ' =', value)
    
    return q

def get(cls, count=1, **kwargs):
    q = constrain(cls, **kwargs)
    
    if count == 1:
        return q.get()
        
    if count > 1:
        return q.fetch(count)
        
    return q