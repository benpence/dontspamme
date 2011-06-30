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
        mask=to_address.contact)
    
    # Invalid contact mask
    if not contact:
        # TODO: Should we warn user that they have sent invalid contact mask?
        logging.info("Invalid Reply: %s -> ?" % pseudo.email())
        return

    logging.info("Reply: %s -> %s" % (pseudo.email(), contact.email))
    
    # Send message
    self.sanitize(message, pseudo)
    message.sender = pseudo.email()
    message.to = contact.email

    message.send()

def sanitize_message(self, message, pseudo):
    """
    Remove all traces of User's REAL email address from message body.

    Args:
        message: InboundEmailMessage
        pseudo: Pseudonym
    """
    # TODO: Write sanitization

    """
    Something like this:
    message.body.replace(pseudo.user.email(), pseudo.email)
    """
    pass
