#!/usr/bin/env python
"""
    purser :: sanity_test.py
"""

# unit testing module
import unittest

# google app engine imports
from google.appengine.api import mail
from google.appengine.ext import db, webapp
from google.appengine.ext import testbed

# helpers
import logging
from models import *
from paypal_notification_handler import *

class SanityTest(unittest.TestCase):
    def setUp(self):
        self.application = webapp.WSGIApplication([MailHandler.mapping()], debug=True)
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        pass
    
    def tearDown(self):
        # calling the deactivation procedure will cause the unit runner to crash
        # self.testbed.deactivate()
        pass
    
    # =================================
    # testing core ent support
    # =================================

    def testSanity(self):     
        campaign = Campaign(name = "UWCLPC Fundraiser",
                            short_code = "LPCFund",
                            goal = 40000)
        campaign.put()
        
        person = Person(name = "John Smith",
                        email = "john@smith.com")
        person.put()
        
        self.assertEqual(0, campaign.total_raised)
        self.assertEqual(0, person.total_donated)

    def testDonation(self):     
        campaign = Campaign(name = "UWCLPC Fundraiser",
                            short_code = "LPCFund",
                            goal = 40000)
        campaign.put()
        
        person = Person(name = "John Smith",
                        email = "john@smith.com")
        person.put()
        
        donation = Donation(donor = person,
                            campaign = campaign,
                            amount = 10000)
        donation.put()
                            
        self.assertEqual(10000, campaign.total_raised)
        self.assertEqual(10000, person.total_donated)
    
    def testMultipleDonationsByOnePerson(self):     
        campaign = Campaign(name = "UWCLPC Fundraiser",
                            short_code = "LPCFund",        
                            goal = 40000)
        campaign.put()
        
        person = Person(name = "John Smith",
                        email = "john@smith.com")
        person.put()
        
        donation = Donation(donor = person,
                            campaign = campaign,
                            amount = 10000)
        donation.put()
        
        donation = Donation(donor = person,
                            campaign = campaign,
                            amount = 10000)
        donation.put()
                            
        self.assertEqual(20000, campaign.total_raised)
        self.assertEqual(20000, person.total_donated)
    
    def testMultipleDonationsByManyPeople(self):     
        campaign = Campaign(name = "UWCLPC Fundraiser",
                            short_code = "LPCFund",        
                            goal = 40000)
        campaign.put()
        
        person_john = Person(name = "John Smith",
                        email = "john@smith.com")
        
        person_jane = Person(name = "Jane Doe",
                        email = "jane@doe.com")

        person_john.put()
        person_jane.put()
        
        donation_john = Donation(donor = person_john,
                            campaign = campaign,
                            amount = 20000)
        
        donation_jane = Donation(donor = person_jane,
                                campaign = campaign,
                                amount = 25000)
        donation_john.put()
        donation_jane.put()
                            
        self.assertEqual(45000, campaign.total_raised)
        self.assertEqual(20000, person_john.total_donated)
        self.assertEqual(25000, person_jane.total_donated)
    
    def testCompleteCampaign(self):     
        campaign = Campaign(name = "UWCLPC Fundraiser",
                            short_code = "LPCFund",
                            goal = 40000)
        campaign.put()
        
        person = Person(name = "John Smith",
                        email = "john@smith.com")        
        person.put()
        
        donation = Donation(donor = person,
                            campaign = campaign,
                            amount = 40000)
        donation.put()
        
        self.assertTrue(campaign.is_goal_met)
    