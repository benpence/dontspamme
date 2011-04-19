from google.appengine.ext import db

import ext
import exception

class Users(db.Model):
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
    
    """TODO: Decide if domain should be references to Contacts. The only problem is the wildcard. How do I handle that?"""

    user        = db.UserProperty()
    mask        = db.StringProperty(multiline=False)
    
    domain      = db.StringListProperty(multiline=False)
    contact     = db.ReferenceProperty(Peer, collection_name='contacts')
    flag        = db.BooleanProperty()
    
    created     = db.DateTimeProperty(auto_now_add=True)
    
    @classmethod
    def userToPseudonym(cls, user):
        pseudos = cls.gql(
            "WHERE user = :user",
            user=user
        )

        if not pseudos:
            raise exception.EmptyQueryError("No pseudonyms for user" + str(user))

        return pseudos[0]
            
class Contact(db.Model):
    """
    A mapping of a hashstring -> email address.
    Allows the user of the Pseudonym to indicate to whom they are responding.

    Attributes:
        pseudo: Pseudonym object. Represents who this is a contact for.
        tag: str that maps to the email of the contact
        email: the email of the contact
    """

    """TODO: Allow user of Pseudonym to initiate an email conversation. While this is not what the tool was intended for, it should be possible."""
    """TODO: Look into encrypting email mappings for Addresses on the server. Then again, maybe not."""

    pseudo      = db.ReferenceProperty(Pseudonym)
    tag         = db.StringProperty(multiline=False)
    email       = db.StringProperty(multiline=False)

    @classmethod
    def emailToTag(cls, pseudo, email):
        """
        Lookup contact email by sender (user) and received tag.
        User is replying to contact's email.
        """
        tags = cls.gql(
            "WHERE pseudo = :pseudo AND email = :email",
            pseudo=pseudo,
            email=email,
        )

        if not tags:
            raise exception.EmptyQueryError("No tags for email" + email)

        return tags[0]
