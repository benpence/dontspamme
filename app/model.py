from google.appengine.ext import db

import ext

class Users(db.Model):
    """A user associated with this app. Primary function is to disallow other users from using app.

    Attributes:
        user: Google user
        isAdmin: boolean
            True  -> can add and remove users
            False -> cannot add/remove
    """

    user        = db.UserProperty()
    isAdmin     = db.StringProperty(multiline=False)

class Pseudonym(db.Model):
    """A pseudonym (mask) for a user.

    Attributes:
        user: Owner of pseudonym
        mask: Pseudonym string. example: a38g70a@mycrazyapp.appspot.com
        domains: Legitimate domain(s). Filled in on creation.
        contact/contacts: Collection of contacts associated with this pseudonym
        flag: boolean
            True  -> flag emails from invalid contacts
            False -> don't
        created: datetime of creation time
    """
    
    """TODO: Decide if domain should be references to Contacts. The only problem is the wildcard. How do I handle that?"""

    user        = db.UserProperty()
    mask        = db.StringProperty(multiline=False)
    
    domain      = db.StringListProperty(multiline=False)
    contact     = db.ReferenceProperty(Peer, collection_name='contacts')
    flag        = db.BooleanProperty()
    
    created     = db.DateTimeProperty(auto_now_add=True)
    
    @classmethod
    def user_pseudonyms(cls, user):
        return cls.gql(
            "WHERE user = :user ORDER BY created ASC",
            user=user
        )
            
class Contact(db.Model):
    """
    A mapping of a hashstring -> email address.
    Allows the user of the Pseudonym to indicate to whom they are responding.
    """

    """TODO: Allow user of Pseudonym to initiate an email conversation. While this is not what the tool was intended for, it should be possible."""
    """TODO: Look into encrypting email mappings for Addresses on the server. Then again, maybe not."""

    pseudo = db.ReferenceProperty(Pseudonym, collection_name='tags')
    tag = db.StringProperty(multiline=False)
    address = db.StringProperty(multiline=False)

    def emailToTag(self):
        pass
        """CHECK IF ALREADY IN DATABASE"""
