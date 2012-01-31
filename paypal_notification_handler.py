#!/usr/bin/env python
# -*- coding: utf-8

# Google App Engine imports
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp.mail_handlers import InboundMailHandler 

# helper handlers imports
import logging, email, re

# import models
from models import *

class MailHandler(InboundMailHandler):
    def receive(self, message):
        logging.info("Received a donation e-mail.")
        
        to_parse = ""
        plaintext_bodies = message.bodies('text/plain')
        for content_type, body in plaintext_bodies:
                to_parse = body.decode()
                logging.info(to_parse)
        
        # obtain the donor's email
        email_unparsed = message.sender
        email_block = re.findall("([\w\-\.+]+@(\w[\w\-]+\.)+[\w\-]+)", email_unparsed)
        email = email_block[0][0]
        logging.info(email)
        
        if re.findall("Kod potwierdzenia", to_parse) or re.findall("service@paypal.pl", email):
            pass
        else:            
            # obtain the donor's name
            p = re.findall(r"nika [\w]* [\w]* \(", to_parse)
            p = p[0][5:-2]
            logging.info(p)
            name = p
        
            # obtain the donation's amount
            p = re.findall("ci [0-9]*,[0-9]* PLN", to_parse)
            p = p[0]
            p = re.findall("\d", p)
            p = ''.join(p)
            logging.info(p)
            amount = int(p)
        
            # obtain the donation key
            p = re.findall("cy: [\w]*", to_parse)
            logging.info(p)
            p = p[0][4:]
            p = ''.join(p)
            logging.info(p)
            donation_key = p
        
            # obtain the campaign key
            p = re.findall(r"2012Fund", to_parse)
            if p:
                key = "2012Fund"
            else:
                key = "default"
        
            # process the data
            campaign = Campaign.get_by_key_name(key)
        
            if not campaign:
                # we didn't find the matching campaign, we will have to pull default
                campaign = Campaign.get_by_key_name(key)
                if not campaign:
                    # the default campaign seems to not be there, spawn one
                    campaign = Campaign(key_name = key,
                                        short_code = key,
                                        name = "Default fundraising campaign",
                                        goal = 0,
                                        starting_from = 0)
                    campaign.put()
        
            person = Person.get_by_key_name(email)
        
            if not person:
                person = Person(key_name = email,
                                name = name,
                                email = email)
                person.put()
        
            donation = Donation.get_by_key_name(donation_key)
        
            if not donation:
                donation = Donation(key_name = donation_key,
                                    parent = person,
                                    donor = person,
                                    campaign = campaign,
                                    amount = amount)
                donation.put()
        
            # time for some channel voodoo?
        
            
def main():
    application = webapp.WSGIApplication([MailHandler.mapping()],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
