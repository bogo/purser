#!/usr/bin/env python
"""
    purser :: campaign.py
"""
# Google App Engine handlers
from google.appengine.ext import db

# helper handlers
import logging
import simplejson as json
import datetime

from decimal import *

# purser imports
# from donation import Donation

def moneyfmt(value, places=0, curr='', sep=' ', dp='',
             pos='', neg='-', trailneg=''):
    q = Decimal(10) ** -places      # 2 places --> '0.01'
    sign, digits, exp = value.quantize(q).as_tuple()
    result = []
    digits = map(str, digits)
    build, next = result.append, digits.pop
    if sign:
        build(trailneg)
    for i in range(places):
        build(next() if digits else '0')
    build(dp)
    if not digits:
        build('0')
    i = 0
    while digits:
        build(next())
        i += 1
        if i == 3 and digits:
            i = 0
            build(sep)
    build(curr)
    build(neg if sign else pos)
    return ''.join(reversed(result))


class Campaign(db.Model):
    name = db.StringProperty(required = True)
    short_code = db.StringProperty(required = True)
    goal = db.IntegerProperty(default = 0)      # specifies campaign goal, if 0 is infinite
    starting_from = db.IntegerProperty(default = 0)
    
    started_at = db.DateProperty(auto_now_add=True)
    deadline = db.DateProperty(default = datetime.date.today()+datetime.timedelta(days=14))
    
    @property
    def total_raised(self):
        total_amount_raised = self.starting_from
        for donation in self.donations:
            total_amount_raised += donation.amount
        return total_amount_raised
    
    @property
    def total_missing(self):
        if self.goal:
            return (self.goal - self.total_raised)
            
    @property
    def total_missing_in_currency_units(self):
        # return "%.2f" % (float(self.total_missing)/100)
        return moneyfmt(Decimal(int(self.total_missing)/100))         
        
    @property
    def percent_left(self):
        percentage_missing = float(self.total_missing)/self.goal*100
        return percentage_missing
        
    @property
    def is_goal_met(self):
        if self.total_raised >= self.goal:
            return True
        else:
            return False
    
    @property
    def goal_in_currency_units(self):
        return moneyfmt(Decimal(int(self.goal/100)))

    @property
    def total_raised_in_currency_units(self):
        return moneyfmt(Decimal(int(self.total_raised/100)))
    
    # @property
    # def list_last_donations(self, number=5):
    #     try:
    #         donation = self.donations[0]
    #         query = donation.all().filter("campaign =", self.key()).order("-date")
    #         result = query.fetch(limit=number)
    #     except:
    #         result = []
    #     finally:
    #         return result
        