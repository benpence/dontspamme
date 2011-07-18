import logging
import json
import re

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

import dontspamme.model as model
from dontspamme.web.authenticate import AuthenticatedRequest
import dontspamme.web.api.decorate as decorate
import dontspamme.web.api.constraint as constraint
import dontspamme.web.api.exception as exception
    
class APIHandler(webapp.RequestHandler):
    pass
    
class MemberHandler(APIHandler):
    @decorate.is_admin
    @decorate.read_options('user')
    def get(self, member, *exposed_arguments):
        return model.Member.all()
    
    @decorate.is_admin
    @decorate.write_options(email=constraint.is_valid_email)
    def add(self, member, email=None):
        new_member = model.Member(user=users.User(email))
        new_member.put()

    @decorate.is_admin
    @decorate.write_options(email=constraint.is_valid_email)
    def remove(self, member, email=None):
        remove_member = model.get(
            model.Member,
            email=email
        )
        
        if not remove_member:
            raise exception.APINoKeyError("Member")
        
        if remove_member.user.email() == member.email():
            raise exception.APIValueContraintError("Member: cannot remove yourself")
            
        for pseudo in remove_member.pseudonyms:
            for contact in pseudo.contacts:
                contact.delete()
            pseudo.delete()
        remove_member.delete()
    
class PseudonymHandler(APIHandler):
    @decorate.is_member
    @decorate.read_options('mask', 'domains', 'should_drop', mask=str)
    def get(self, member, *exposed_arguments, mask=None):
        return model.get(model.Pseudonym, member=member, mask=mask)
    
    @decorate.is_member
    @decorate.write_options(mask=str, domain=constraint.is_valid_domain)
    def add(self, member, mask=None, domain=None):
    
    @decorate.is_member    
    @decorate.write_options(mask=str, domain=constraint.is_valid_domain)
    def remove(self, member, mask=None, domain=None):
        
    
    @decorate.is_member    
    @decorate.write_options(mask=str, should_drop=bool)
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
    @decorate.write_options(mask=str, domain=constraint.is_valid_domain)
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
    @decorate.write_options(mask=str, domain=constraint.is_valid_domain)
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