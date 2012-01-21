#!/usr/bin/env python
"""
    purser :: person_controller.py
"""

# Google App Engine handlers
from google.appengine.ext import webapp, db

# helper handlers
import logging
import simplejson as json

# Tuk-Tuk imports
from models import Person
# from views import PersonView

class PersonController(webapp.RequestHandler):
    def get(self):
        # campaign = Campaign.get_by_key_name(campaign_id)
        # if campaign:
        #     status_view = CampaignStatusView(campaign = campaign, response = self.response)
        pass
            
    def post(self):
        email = self.request.get("email")
        name = self.request.get("name")
        person = Person.get_by_key_name(name)
        if not person:
            person = Person(key_name = email,
                            email = email,
                            name = name)
            person.put()
        