import os

# Where non-users are referred to if they're logged in
referral_for_non_users = "<<REFERRAL_FOR_NON_USERS>>" 

# The subject-prefix of messages that have been flagged as spam
spam_label = '<<SPAM_SUBJECT_PREFIX>>'

# App domains
app = os.getcwd().split('/')[-2]

DEBUG = True
web_domain = app + '.appspot.com'
mail_domain = app + '.appspotmail.com'