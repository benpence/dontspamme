from google.appengine.ext import db

import dontspamme.util as util
import dontspamme.config

class User(db.Model):
    """
    A user associated with this app. Primary function is to disallow other
    users from using app.

    Attributes:
        user: Google user
    """
    user        = db.UserProperty()

class Contact(db.Model):
    """
    Prototype
    """
    pass

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
    user          = db.UserProperty()
    mask          = db.StringProperty(default=util.generate_random_string(), multiline=False)    

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
    mask        = db.StringProperty(default=util.generate_random_string(), multiline=False)
    
    email       = db.StringProperty(multiline=False)
    name        = db.StringProperty(multiline=False)
    
    created     = db.DateTimeProperty(auto_now_add=True)

def get(cls, count=None, **kwargs):
    q = cls.all()

    for key, value in kwargs.items():
        q.filter(key + ' =', value)
    
    if count:
        return q.fetch(count)

    return q.get()
