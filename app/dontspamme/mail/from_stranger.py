import logging
import os

import dontspamme.util as util
import dontspamme.model as model
import dontspamme.config
from dontspamme.mail import LINK_REMOVE_CLASS

def handle(message, pseudo, stranger_address):
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
    new_prefix = ''
    if not contact:
        contact = model.Contact(
            pseudonym=pseudo,
            email=stranger_address.email,
            mask=util.generate_random_string(),
            name=stranger_address.name
        )
        contact.put()
        
        new_prefix = 'New '

    logging.info("%sContact: %s -> %s" % (
        new_prefix,
        stranger_address.email,
        pseudo.email
    ))

    # Test for spam and add link generation
    should_drop = prepare_message(
        message,
        pseudo,
        stranger_address,
        is_spam=stranger_address.domain not in pseudo.domains
    )
    if should_drop:
        return

    message.to = pseudo.user.email()

    # This is important because it lets the user know WHO EMAILED THEM
    message.sender = "'%s <%s>' <%s+%s@%s>" % (
        # ie "'Bob Frizzel <bob@frizzel.net>' <x2c38+c8238@myapp.appspotmail.com>"
        contact.name,
        contact.email,

        pseudo.mask,
        contact.mask,
        dontspamme.config.domain_name
    )

    logging.info("Body ======== \n%s" % message.html.decode())
    message.send()

def prepare_message(message, pseudo, stranger_address, is_spam=False):
    """
    Add header to message body.

    Args:
        message: InboundEmailMessage
        pseudo: Pseudoynm of recipient
        domain: domain of sender
        isSpam: bool = did the message came from one of pseudo's domains
    """
    # Not spam
    if not is_spam:
        return
    
    # Drop spam
    if pseudo.should_drop:
        return True
        
    # Mark as spam
    message.subject = dontspamme.config.spam_label + ' ' + message.subject
    
    add_domain_link = create_link(
        stranger_address.email + ' is not spam',
        'adddomain',
        mask=pseudo.mask,
        domain=stranger_address.domain
    )
    
    body = message.html.decode()    
    body = add_domain_link + '\n' + body
    message.html = body.encode()
    
def create_link(title, action, **kwargs):
    """
    Generate link for performing actions via GET requests
    """
    logging.info(LINK_REMOVE_CLASS)
    return "<a class=\"%s\" href=\"%s\">%s</a>" % (
        # Tag for removing later
        LINK_REMOVE_CLASS,
        
        # Generated link URL
        '/'.join((
            'http' + dontspamme.config.domain_name,
            action + util.make_get_arguments(**kwargs)
        )),
        
        # Visible anchor text
        title
    )