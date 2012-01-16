#!/usr/bin/env python
"""
    purser :: donation.py
"""
# Google App Engine handlers
from google.appengine.ext import db

# helper handlers
import logging
import simplejson as json

# purser imports
from campaign import Campaign
from person import Person

class Donation(db.Model):
    date = db.DateTimeProperty(auto_now_add = True)
    donor = db.ReferenceProperty(Person, collection_name = "donations", required = True)
    campaign = db.ReferenceProperty(Campaign, collection_name = "donations")
    amount = db.IntegerProperty(default = 0, required = True)
    # currency = 
    
    @property
    def date_plain(self):
        return "%4d-%02d-%02d" % (self.date.year, self.date.month, self.date.day)
        
    @property
    def amount_in_currency_units(self):
        return "%.2f" % (int(self.amount/100))
    