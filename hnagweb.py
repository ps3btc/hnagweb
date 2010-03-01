#!/usr/bin/env python
#
# Copyright 2010 Hareesh Nagarajan.

__author__ = 'hareesh.nagarajan@gmail.com (Hareesh Nagarajan)'

import os
import logging
import wsgiref.handlers
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.api import memcache

HOMEPAGE_KEY = "homepage"
CREDITS_KEY = "credits"
MEMCACHE_EXPIRE = 864000

class FlushMemcache(webapp.RequestHandler):
  def get(self):
    if memcache.flush_all():
      logging.info('memcache: flushed all')
      self.redirect('/', permanent=False)

class Home(webapp.RequestHandler):
  def get(self):
    homepage = memcache.get(HOMEPAGE_KEY)
    if homepage:
      self.response.out.write(homepage)
      return
    
    path = os.path.join(os.path.dirname(__file__), 'index.html')
    template_values = {}
    render_page = template.render(path, template_values)
    memcache.add(HOMEPAGE_KEY, render_page, MEMCACHE_EXPIRE)
    logging.info('did not find homepage in memcache; inserting ...')
    self.response.out.write(template.render(path, {}))
     
class Credits(webapp.RequestHandler):
  def get(self):
    page = memcache.get(CREDITS_KEY)
    if page:
      self.response.out.write(page)
      return
    
    path = os.path.join(os.path.dirname(__file__), 'credits.html')
    template_values = {}
    render_page = template.render(path, template_values)
    memcache.add(CREDITS_KEY, render_page, MEMCACHE_EXPIRE)
    logging.info('did not find credits in memcache; inserting ...')
    self.response.out.write(template.render(path, {}))

def main():
  application = webapp.WSGIApplication([
      ('/', Home),
      ('/credits', Credits),
      ('/flushmemcache', FlushMemcache),
      ], debug=True)
  wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
  main()
