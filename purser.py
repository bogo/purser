#!/usr/bin/env python
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from controllers import *

if __name__ == "__main__":
    application = webapp.WSGIApplication(purser, debug=True)
    run_wsgi_app(application)
    
