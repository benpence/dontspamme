from google.appengine.ext import db

class Pseudonym(db.Model):
    owner = db.UserProperty()
    mask = db.StringProperty(multiline=False)
    
    domain = db.StringProperty(multiline=False)
    
    created = db.DateTimeProperty(auto_now_add=True)
    
    def user_pseudonyms(cls, user):
        return cls.gql(
            "WHERE owner = :owner ORDER BY created ASC",
            owner=owner)
            
class Address(db.Model):
    pseudo = db.ReferenceProperty(Pseudonym,
                                  collection_name='tags')
    tag = db.StringProperty(multiline=False)
    address = db.StringProperty(multiline=False)
    
    def __init__(self):
        tag = self.generate_tag()
    
    @classmethod
    def generate_tag(self):
        # CHECK IF ALREADY IN DATABASE
        pass