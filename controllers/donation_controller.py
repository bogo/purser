#!/usr/bin/env python
"""
    purser :: donation_controller.py
"""

# Google App Engine handlers
from google.appengine.ext import webapp, db

# helper handlers
import logging
import simplejson as json

# Tuk-Tuk imports
from models import *
# from views import PersonView

class DonationController(webapp.RequestHandler):
    def get(self):
        # campaign = Campaign.get_by_key_name(campaign_id)
        # if campaign:
        #     status_view = CampaignStatusView(campaign = campaign, response = self.response)
        pass
            
    def post(self):
        campaign_key = self.request.get("campaign_key")
        person_key = self.request.get("person_key")
        amount = self.request.get("amount")
        
        person = Person.get_by_key_name(person_key)
        campaign = Campaign.get_by_key_name(campaign_key)
        
        donation = Donation(donor = person,
                            campaign = campaign,
                            amount = int(amount))
        
        donation.put()