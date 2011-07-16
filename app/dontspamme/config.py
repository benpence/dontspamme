# Where non-users are referred to if they're logged in
referral_for_non_users = "www.google.com" 

# The subject-prefix of messages that have been flagged as spam
spam_label = '(SPAM)' 


# CHANGE THESE IF YOU KNOW WHAT YOU'RE DOING
app = os.getcwd().split('/')[-2]
web_domain = app + '.appspot.com'
mail_domain = app + '.appspotmail.com'