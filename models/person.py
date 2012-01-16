#!/usr/bin/env python
"""
    purser :: person.py
"""
# Google App Engine handlers
from google.appengine.ext import db

# helper handlers
import logging
import simplejson as json

# purser imports
# from donation import Donation


class Person(db.Model):
    name = db.StringProperty(required = True)
    email = db.EmailProperty(required = True)

    @property
    def total_donated(self):
        total_amount_donated = 0
        for donation in self.donations:
            total_amount_donated += donation.amount
        return total_amount_donated
