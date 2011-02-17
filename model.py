from google.appengine.ext import db

class Pseudonym(db.Model):
    user = db.UserProperty()
    recv_mask = db.StringProperty(multiline=False)
    send_mask = db.StringProperty(multiline=False)
    domain = db.StringProperty(multiline=False)
    created = db.DateTimeProperty(auto_now_add=True)
    
    def user_pseudonyms(cls, user):
        return cls.gql(
            "WHERE user = :user ORDER BY created ASC",
            user=user)