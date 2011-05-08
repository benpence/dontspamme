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

class Contact(db.Model):
    pass

class Pseudonym(db.Model):
    """
    A pseudonym (mask) for a user.

    Attributes:
        user: Owner of pseudonym
        mask: Pseudonym string. example: a38g70a
        domain/domains: Legitimate domain(s).
        contact/contacts: Collection of contacts associated with this pseudonym
        should_filter: boolean
            True  -> flag emails from invalid contacts
            False -> don't
        created: datetime of creation time
    """
    
    user          = db.UserProperty()
    mask          = db.StringProperty(multiline=False)    

    domains       = db.StringListProperty()
    contact       = db.ReferenceProperty(Contact, collection_name='contacts')
    should_filter = db.BooleanProperty()
    
    created       = db.DateTimeProperty(auto_now_add=True)
            
class Contact(db.Model):
    """
    A mapping of a hashstring -> email address.
    Allows the user of the Pseudonym to indicate to whom they are responding.

    Attributes:
        pseudonym: Pseudonym object. Represents who this is a contact for.
        mask: str that maps to the email of the contact
        email: the email of the contact ex: steve@corp.microsoft.com
    """

    # TODO: Allow user of Pseudonym to initiate an email conversation.
    # While this is not what the tool was intended for, it should be possible.

    pseudonym   = db.ReferenceProperty(Pseudonym)
    mask        = db.StringProperty(multiline=False)
    email       = db.StringProperty(multiline=False)

def get(cls, count=None, **kwargs):
    q = cls.all()
    for k,v in kwarags:
        q.filter(k+" =",v)
    
    if count:
        return q.fetch(count)
    return q.get()

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