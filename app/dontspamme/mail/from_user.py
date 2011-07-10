import logging

import dontspamme.model as model

def from_user(message, pseudo, to_address):
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
    Remove all traces of User's REAL email address from message body.

    Args:
        message: InboundEmailMessage
        pseudo: Pseudonym
        to_address: EmailAddress
        contact: reply to Contact 
    """
    # TODO: Refine sanitization to be more flexible (regexes?)
    for content_type in ('body', 'html'):
        body = getattr(message, content_type).decode()

        # Remove traces of real email address (ie quoted reply)
        body = body.replace(pseudo.user.email(), pseudo.email)
        
        # If message is quoted in reply, don't reveal reply-address
        body = body.replace(to_address.original, contact.email).encode()
        
        setattr(message, content_type, body)