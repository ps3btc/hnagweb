#!/usr/bin/env python
#
# Copyright 2010 Hareesh Nagarajan.

__author__ = 'hareesh.nagarajan@gmail.com (Hareesh Nagarajan)'

import os
import logging
import wsgiref.handlers
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

class Home(webapp.RequestHandler):
  def get(self):
    path = os.path.join(os.path.dirname(__file__), 'index.html')
    self.response.out.write(template.render(path, {}))
     
class Credits(webapp.RequestHandler):
  def get(self):
    path = os.path.join(os.path.dirname(__file__), 'credits.html')
    self.response.out.write(template.render(path, {}))

class Feedback(webapp.RequestHandler):
  def get(self):
    path = os.path.join(os.path.dirname(__file__), 'feedback.html')
    self.response.out.write(template.render(path, {}))

def main():
  application = webapp.WSGIApplication([
      ('/', Home),
      ('/credits', Credits),
      ('/feedback', Feedback),
      ], debug=True)
  wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
  main()
