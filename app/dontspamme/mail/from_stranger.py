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
            name=stranger_address.name,
            mask=util.generate_random_string(),
        )
        contact.put()
        
        new_prefix = 'New '

    logging.info("MAIL: %sContact: %s -> %s" % (
        new_prefix,
        stranger_address.email,
        pseudo.email
    ))

    # Test for spam and add link generation
    should_drop = prepare_message(
        message,
        pseudo,
        stranger_address,
    )
    if should_drop:
        return

    message.to = pseudo.member.user.email()

    # This is important because it lets the user know WHO EMAILED THEM
    message.sender = "'%s <%s>' <%s+%s@%s>" % (
        # ie "'Bob Frizzel <bob@frizzel.net>' <x2c38+c8238@myapp.appspotmail.com>"
        contact.name,
        contact.email,

        pseudo.mask,
        contact.mask,
        dontspamme.config.mail_domain
    )

    logging.debug("Body ======== \n%s" % message.html.decode())
    message.send()

def prepare_message(message, pseudo, stranger_address):
    """
    Add header to message body.

    Args:
        message: InboundEmailMessage
        pseudo: Pseudoynm of recipient
        domain: domain of sender
    """
    
    is_spam = stranger_address.domain not in pseudo.domains
    
    # Not spam
    if not is_spam:
        return
    
    # Drop spam
    if pseudo.should_drop:
        logging.info("MAIL: SPAM dropped")
        return True
    
    logging.info("MAIL: SPAM flagged")
        
    # Mark as spam
    message.subject = dontspamme.config.spam_label + ' ' + message.subject
    
    # Link for adding domain to 'not spam' list
    add_domain_link = create_link(
        'Mail from ' + stranger_address.domain + ' is not spam',
        'adddomain',
        mask=pseudo.mask,
        domain=stranger_address.domain
    )
    
    body = message.html.decode()    
    body = add_domain_link + '<br />' + body
    message.html = body.encode()
    
def create_link(title, action, **kwargs):
    """
    Generate link for performing actions via GET requests
    """
    return "<a class=\"%s\" href=\"%s\">%s</a>" % (
        # Tag for removing later
        LINK_REMOVE_CLASS,
        
        # Generated link URL
        '/'.join((
            util.prepend_if_absent('http://', dontspamme.config.web_domain),
            action + util.make_get_arguments(**kwargs)
        )),
        
        # Visible anchor text
        title
    )