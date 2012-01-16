#!/usr/bin/env python
"""
    purser :: campaign_status_view.py
"""
# Google App Engine handlers
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util

# Google App Engine handlers for templating
import os
from google.appengine.ext.webapp import template

# helper handlers
import simplejson as json
import logging
import os

# Tuk-Tuk imports
from models import Campaign

class CampaignStatusView:
    def __init__(self, campaign=None, response=None):
        template_values =   {
                                'campaign' : campaign
                            }
        path = os.path.join(os.path.dirname(__file__), 'campaign_status_template.html')
        response.out.write(template.render(path, template_values))