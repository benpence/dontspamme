import logging

import dontspamme.model as model

def from_user(self, message, pseudo, to_address):
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
        logging.info("Invalid Reply: %s -> ?" % pseudo.email())
        return

    logging.info("Reply: %s -> %s" % (pseudo.email(), contact.email))
    
    # Send message
    self.sanitize(message, pseudo, to_address, contact)

    message.sender = pseudo.email()
    message.to = contact.email

    message.send()

def sanitize_message(self, message, pseudo, to_address, contact):
    """
    Remove all traces of User's REAL email address from message body.

    Args:
        message: InboundEmailMessage
        pseudo: Pseudonym
        to_address: EmailAddress
        contact: reply to Contact 
    """
    # TODO: Refine sanitization to be more flexible (regexes?)

    # Remove traces of real email address (ie quoted reply)
    message.body.replace(pseudo.email, pseudo.email)

    # If message is quoted in reply, don't reveal reply-address
    message.body.replace(to_address.original, contact.email)
