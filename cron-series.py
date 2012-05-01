import urllib
import os
import cgi
import datetime
import commonstrings
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from google.appengine.ext import db
from google.appengine.api import mail
from google.appengine.api import datastore_types

class MainPage(webapp.RequestHandler):
    def get(self):	
		start = datetime.datetime.now()
		self.response.out.write("Starting at " + start.isoformat())
		
		
		#-------------------------------------------------------------------
		# This searches for all listed series and 
		#-------------------------------------------------------------------
		checkseries = []
		q = db.GqlQuery("SELECT * FROM SeriesSearch")
		results = q.fetch(100)
		for entry in results:
			#self.response.out.write("<br /> checking: " + entry.seriesname + ", ")
			if not entry.seriesname in checkseries: 
				checkseries.append(entry.seriesname.lower())
				self.response.out.write("<br /> adding to array: " + entry.seriesname + ", ")
		
		for series in checkseries: 
			seriestocheck = SeriesToCheck(seriesname=series)
			seriestocheck.put()
		
		end = datetime.datetime.now() 
		tdelta = end - start
		self.response.out.write("<br />Ending at " + end.isoformat())
		self.response.out.write("<br />--------<br />Time taken " + str(tdelta))

# ----------------------------------------------------
# Set up the data
# ----------------------------------------------------	
class ChannelsToCheck(db.Model):
	channelnumber = db.StringProperty()	
class SeriesToCheck(db.Model):
	seriesname = db.StringProperty()		
class SeriesSearch(db.Model):
	channels = db.StringProperty()
	seriesname = db.StringProperty()
	emailto = db.StringProperty()
	checked = db.DateTimeProperty()
		
application = webapp.WSGIApplication(
                                     [('/cron/series', MainPage)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()