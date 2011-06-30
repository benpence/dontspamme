import logging

import dontspamme.util as util
import dontspamme.model as model
import dontspamme.config

def from_stranger(self, message, pseudo, stranger_address):
    """
    Stranger emailing a pseudonym
    New strangers will be added as Contact.
    Strangers sending from invalid domain will be flagged.

    Args:
        message: InboundEmailMessage
        pseudo: Pseudonym of user
        stranger_email: str in 'x@x' format
    """
    contact = model.get(
        model.Contact,
        pseudonym=pseudo,
        email=stranger_address.email
    )

    # Create entry if new
    if not contact:
        contact = model.Contact(
            pseudonym=pseudo,
            email=stranger_address.email,
            mask=util.generate_random_string()
        )
        contact.put()

        logging.info("New Contact")

    logging.info("Contact: %s -> %s" % (
        stranger_address.email,
        pseudo.email(),
    ))


    # Send response
    prepare_message(
        message,
        pseudo,
        isSpam=stranger_address.domain not in pseudo.domains
    )

    message.to = pseudo.user.email()
    message.sender = "<%s+%s@%s>" % (
        pseudo.mask,
        contact.mask,
        dontspamme.config.domain_name
    )

    # TODO: Clear rest of fields to avoid exposing username on cc, bcc?
    message.send()

def prepare_message(self, message, pseudo, isSpam=False):
    """
    Add header to message body.

    Args:
        message: InboundEmailMessage
        pseudo: Pseudoynm of recipient
        isSpam: bool = did the message came from one of pseudo's domains
    """
    # TODO: Add link generation for adding this domain to pseudo.domains
    
    if isSpam and pseudo.should_filter:
        message.subject = dontpsamme.config.spam_label + ' ' + message.subject