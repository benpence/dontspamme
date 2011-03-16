def email_split(email, start='', end=''):
    partition = email[email.rfind(start): email.rfind(end)]

    if not partition:
        return None

    return partition[1:]
        
hey = [
    ('hey+ho@dd.com', '+', '@'),
    ('okay@donkey.net', '@', ''),
    ('dondondon+ee+fff@ell.com', '+', '@'),
    ('my_best_friend+ee+ee+ff@spidermonkeys.com', '+', '')
    ]
 
 
for string, start, end in hey:
    print string, start, end, email_split(string, start, end)