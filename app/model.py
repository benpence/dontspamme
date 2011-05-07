import random

from google.appengine.ext import db

class User(db.Model):
    """
    A user associated with this app. Primary function is to disallow other users from using app.

    Attributes:
        user: Google user
        isAdmin: boolean
            True  -> can add and remove users
            False -> cannot add/remove
    """
    user        = db.UserProperty()
    isAdmin     = db.BooleanProperty()

class Pseudonym(db.Model):
    """
    A pseudonym (mask) for a user.

    Attributes:
        user: Owner of pseudonym
        mask: Pseudonym string. example: a38g70a@mycrazyapp.appspot.com
        domain/domains: Legitimate domain(s).
        contact/contacts: Collection of contacts associated with this pseudonym
        flag: boolean
            True  -> flag emails from invalid contacts
            False -> don't
        created: datetime of creation time
    """
    
    # TODO: Decide if domain should be references to Contacts. 
    # The only problem is the wildcard. How do I handle that?

    user        = db.UserProperty()
    mask        = db.StringProperty(multiline=False)
    
    domain      = db.StringListProperty()#multiline=False)
    #contact     = db.ReferenceProperty(Contact, collection_name='contacts')
    flag        = db.BooleanProperty()
    
    created     = db.DateTimeProperty(auto_now_add=True)
            
class Contact(db.Model):
    """
    A mapping of a hashstring -> email address.
    Allows the user of the Pseudonym to indicate to whom they are responding.

    Attributes:
        pseudo: Pseudonym object. Represents who this is a contact for.
        tag: str that maps to the email of the contact
        email: the email of the contact
    """

    # TODO: Allow user of Pseudonym to initiate an email conversation.
    # While this is not what the tool was intended for, it should be possible.
    
    # TODO: Look into encrypting email mappings for Addresses on the server. Then again, maybe not.

    pseudo      = db.ReferenceProperty(Pseudonym)
    tag         = db.StringProperty(multiline=False)
    email       = db.StringProperty(multiline=False)

def where(cls, count=0, **kwargs):
    results = cls.gql(
        "WHERE %s" % ' AND '.join(
            ("%s = :%s" % (key, key) for key in kwargs)
        ),
        **kwargs
    )

    if count:
        return results.fetch(count)

    return results

random.seed()
def random_hash(length):
    """
    Return random hash with 'length' characters
    """

    # TODO: Evaluate different random functions in python by efficiency.
    # Collision resistance is quite unimportant though
    # TODO: Look into running cron jobs to pre-generate N random hashes
    
    return "%x" % random.getrandbits(length * 4)
