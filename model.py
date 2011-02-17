from google.appengine.ext import db

class Pseudonym(db.Model):
    user = db.UserProperty()
    mask = db.StringProperty(multiline=False)
    
    domain = db.StringProperty(multiline=False)
    
    created = db.DateTimeProperty(auto_now_add=True)