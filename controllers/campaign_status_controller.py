#!/usr/bin/env python
"""
    purser :: campaign_status_controller.py
"""

# Google App Engine handlers
from google.appengine.ext import webapp, db

# helper handlers
import logging
import simplejson as json

# Tuk-Tuk imports
from models import Campaign
from views import CampaignStatusView

class CampaignStatusController(webapp.RequestHandler):
    def get(self, campaign_id):
        campaign = Campaign.get_by_key_name(campaign_id)
        if campaign:
            status_view = CampaignStatusView(campaign = campaign, response = self.response)
    
    def post(self, campaign_id):
        campaign = Campaign.get_by_key_name(campaign_id)
        if not campaign:
            campaign =  Campaign(key_name = campaign_id,
                                name = campaign_id,
                                short_code = campaign_id)
            campaign.put()
            status_view = CampaignStatusView(campaign = campaign, response = self.response)
        