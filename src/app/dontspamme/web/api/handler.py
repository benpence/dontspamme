import json
import re
import logging

from google.appengine.ext import webapp

import dontspamme.util as util
import dontspamme.model as model
from dontspamme.web.authenticate import AuthenticatedRequest
from dontspamme.web.api import exception, constraint, decorate
from dontspamme.web.api.meta import APIHandlerFactory

class APIHandler(AuthenticatedRequest):
    """
    Metaclass redirects post requests to the appropriate method in the handler
    """
    __metaclass__ = APIHandlerFactory
    
    def writeout(self, dictionary):
        self.response.out.write(json.dumps(dictionary))

    def error(self, message):
        self.writeout({'error': message})
    
    def make_results_tree(self, results, exposed_arguments):
        return dict((
            # Each object
            (str(result.key()), dict((
                # Each object attribute
                (exposed_argument, str(getattr(result, exposed_argument)))
                for exposed_argument in exposed_arguments
            )))
            for result in results
        ))
            
class MemberHandler(APIHandler):
    @decorate.is_admin
    @decorate.read_options('user')
    def read(self, member, *exposed_arguments):
        self.output = model.Member.all(), exposed_arguments
    
    @decorate.is_admin
    @decorate.write_options(email=constraint.is_valid_email)
    def add(self, member, email=None):
        new_member = model.Member(user=users.User(email))
        new_member.put()

    @decorate.is_admin
    @decorate.write_options(email=constraint.is_valid_email)
    def remove(self, member, email=None):
        member_to_remove = model.get(
            model.Member,
            email=email
        )
        
        if not member_to_remove:
            raise exception.APINoKeyError("Member")
        
        if member_to_remove.user.email() == member.email():
            raise exception.APIValueContraintError("Member: cannot remove yourself")
            
        for pseudo in member_to_remove.pseudonyms:
            for contact in pseudo.contacts:
                contact.delete()
            pseudo.delete()
        member_to_remove.delete()
    
class PseudonymHandler(APIHandler):
    @decorate.is_member
    @decorate.read_options('mask', 'domains', 'should_drop', mask=constraint.is_of_length(util.DEFAULT_LENGTH))
    def read(self, member, *exposed_arguments, **filters):
        self.output = model.get(model.Pseudonym, count=0, member=member, **filters), exposed_arguments
    
    @decorate.is_member
    @decorate.write_options(domain=constraint.is_valid_domain)
    def add(self, member, domain=None):
        pseudo = model.Pseudonym(
            mask=util.generate_random_string(),
            member=member,
            domain=[domain.lower()]
        )
        pseudo.put()
    
    @decorate.is_member    
    @decorate.write_options(mask=constraint.is_of_length(util.DEFAULT_LENGTH))
    def remove(self, member, mask=None):
        pseudo = model.get(
            mask=mask,
            member=member
        )
        
        if not pseudo:
            raise exception.APINoKeyError("Pseudonym")

        for contact in pseudo.contacts():
            contacts.delete()
        pseudo.delete()
    
    @decorate.is_member    
    @decorate.write_options(mask=constraint.is_of_length(util.DEFAULT_LENGTH), should_drop=constraint.is_boolean)
    def drop(self, member, mask=None, should_drop=None):
        pseudo = model.get(
            model.Pseudonym,
            member=member,
            mask=mask
        )
        
        if not pseudo:
            raise exception.APINoKeyError("Pseudonym")
        
        pseudo.should_drop = should_drop
        pseudo.put()

class DomainHandler(APIHandler):
    @decorate.is_member
    @decorate.write_options(mask=constraint.is_of_length(util.DEFAULT_LENGTH), domain=constraint.is_valid_domain)
    def add(self, member, mask=None, domain=None):
        pseudo = model.get(
            model.Pseudonym,
            member=member,
            mask=mask
        )
        
        if not pseudo:
            raise exception.APINoKeyError("Domain")
        
        pseudo.domains.append(domain)
        pseudo.put()

    @decorate.is_member
    @decorate.write_options(mask=constraint.is_of_length(util.DEFAULT_LENGTH), domain=constraint.is_valid_domain)
    def remove(self, member, mask=None, domain=None):
        pseudo = model.get(
            model.Pseudonym,
            member=member,
            mask=mask
        )
        
        if not pseudo:
            raise exception.APINoKeyError("Domain")
            
        domain = domain.lower()
        if len(pseudo.domains) <= 1 or domain not in pseudo.domains:
            raise exception.APINoKeyError("Domain")
            
        pseudo.domains.remove(domain)
        pseudo.put()