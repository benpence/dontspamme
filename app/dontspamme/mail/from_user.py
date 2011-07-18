import logging
import re

import dontspamme.model as model
from dontspamme.mail import LINK_REMOVE_CLASS

def handle(message, pseudo, to_address):
    """
    Send reply to contact.
    Sanitize message, verify contact contact mask, send email to contact.
    
    Args:
        message: InboundEmailMessage
        pseudo: Pseudonym of user
        to_address: recipient
    """
    contact = model.get(
        model.Contact,
        pseudonym=pseudo,
        mask=to_address.contact
    )
    
    # Invalid contact mask
    if not contact:
        # TODO: Should we warn user that they have sent invalid contact mask?
        logging.info("MAIL: Invalid Reply contact: %s+%s -> ?" % (
            pseudo.mask,
            to_address.contact,
        ))
        return 

    logging.info("MAIL: Reply: '%s' -> '%s'" % (pseudo.email, contact.email))
    
    # Send message
    sanitize_message(message, pseudo, to_address, contact)

    message.sender = pseudo.email
    message.to = contact.email

    message.send()

def sanitize_message(message, pseudo, to_address, contact):
    """
    Change fields of message to hide all exposed data

    Args:
        message: InboundEmailMessage
        pseudo: Pseudonym
        to_address: EmailAddress
        contact: reply to Contact 
    """
    replacements = [
        (re.compile(pattern, re.IGNORECASE), replacement)
        for pattern, replacement in (
            # Remove user's real email address
            (re.escape(pseudo.member.user.email()), pseudo.email),
        
            # Remove contact email if message quoted in reply
            (re.escape(to_address.raw), contact.email),
        
            # Remove 'add to not spam list' link from replies
            ('\<a class=\"%s\".+\</a\>\n?' % LINK_REMOVE_CLASS, ''),
        )
    ]
    
    for content_type in ('body', 'html'):
        body = getattr(message, content_type).decode()

        for pattern, replacement in replacements:
            body = pattern.sub(replacement, body)

        logging.debug(body)

        setattr(message, content_type, body.encode())