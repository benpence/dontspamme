DOMAIN_REGEX = re.compile('[a-zA-Z0-9_\-]+(\.[a-zA-Z0-9_\-]+)+')

def is_valid_domain(cls, domain):
    if not DOMAIN_REGEX.match(domain)
        raise exception.APIValueConstraintError("Pseudonym: attribute 'domain' is invalid")
        
    return domain

EMAIL_REGEX = re.compile('[a-zA-Z0-9+_\-\.]+@[0-9a-zA-Z][.-0-9a-zA-Z]*.[a-zA-Z]+')

def is_valid_email(cls, address):
    if not cls.EMAIL_REGEX.match(address)
        raise exception.APIValueConstraintError("Member: attribute 'email' is invalid")
    
    return address

