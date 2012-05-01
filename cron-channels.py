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
	
		# ----------------------------------------------------
		# 1) Find out what channels we need to examine
		# 2) Add them to datastore
		# ----------------------------------------------------	
		start = datetime.datetime.now()
		self.response.out.write("Starting at " + start.isoformat())
		
		# 1) Finding which channels need checking. 
		checkchannels = []
		q = db.GqlQuery("SELECT * FROM SeriesSearch")
		results = q.fetch(500)		
		for entry in results:
			channels = entry.channels
			channel = channels.split("#")
			channel.remove('')
			for singlechannel in channel:
				detail = singlechannel.split("|")
				if not detail[1] in checkchannels: 
					#add to the list of channels we need to examine
					checkchannels.append(detail[1])
					self.response.out.write("<br />" + detail[1] + ", ")
		
		# 2) adding then to db		
		for channel in checkchannels: 
			channelstocheck = ChannelsToCheck(channelnumber=channel)
			channelstocheck.put()
		
			
			

		end = datetime.datetime.now() 
		tdelta = end - start
		self.response.out.write("<br />Ending at " + end.isoformat())
		self.response.out.write("<br />--------<br />Time taken " + str(tdelta))
		
	
	
# ----------------------------------------------------
# Set up the data
# ----------------------------------------------------	
class ChannelsToCheck(db.Model):
	channelnumber = db.StringProperty()	
class SeriesSearch(db.Model):
	channels = db.StringProperty()
	seriesname = db.StringProperty()
	emailto = db.StringProperty()
	checked = db.DateTimeProperty()
		
application = webapp.WSGIApplication(
                                     [('/cron/channels', MainPage)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()