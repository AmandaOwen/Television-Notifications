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
		
		#-------------------------------------------------------------------
		# Clear up the old data store information
		#-------------------------------------------------------------------
		q = db.GqlQuery("SELECT * FROM ChannelsToCheck")
		results = q.fetch(200)		
		for entry in results:
			entry.delete()
		q = db.GqlQuery("SELECT * FROM SeriesToCheck")
		results = q.fetch(200)		
		for entry in results:
			entry.delete()
		q = db.GqlQuery("SELECT * FROM PossiblesToCheck")
		results = q.fetch(200)		
		for entry in results:
			entry.delete()
		self.response.out.write("<br />DONE")

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
class PossiblesToCheck(db.Model):
	ChannelNumber = db.StringProperty()
	SeriesName = db.StringProperty()
	SubTitle = db.StringProperty()
	Episode = db.TextProperty()	
	NewSeries = db.BooleanProperty()	
	Date = db.DateTimeProperty()
	StartTime = db.DateTimeProperty() 
	

	
application = webapp.WSGIApplication(
                                     [('/cron/clearup', MainPage)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()