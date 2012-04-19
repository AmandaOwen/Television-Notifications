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
		# Grabs list of channels from RadioTimes dat file and adds to db
		# Profiles at just over 1 second
		#-------------------------------------------------------------------
		
		channels = commonstrings.GetChannelInformation()
		q = db.GqlQuery("SELECT * FROM ChannelInformation")
		results = q.fetch(500)		
		for entry in results:
			entry.delete()
		for channel in channels: 
			details = channel.split("|")	
			channellisting = ChannelInformation(channelnumber=details[1], channelname=details[0], channelchecked=False)
			channellisting.put()
		q = db.GqlQuery("SELECT * FROM ProgrammeInformation")
		schedule = q.fetch(1000)		
		for prog in schedule:
			prog.delete()
		end = datetime.datetime.now() 
		tdelta = end - start
		self.response.out.write("<br />Ending at " + end.isoformat())
		self.response.out.write("<br />--------<br />Time taken " + str(tdelta))
		
	
	
class ChannelInformation(db.Model):
	channelnumber = db.StringProperty()
	channelname = db.StringProperty()	
	channelchecked = db.BooleanProperty()		
		
	
class ProgrammeInformation(db.Model):
	
	ChannelNumber = db.StringProperty()
	ChannelName = db.StringProperty()	
	ProgrammeTitle = db.StringProperty()
	SubTitle = db.StringProperty()
	Episode = db.StringProperty()
	Year = db.StringProperty()
	Director = db.StringProperty()
	Cast = db.StringProperty()
	Premiere = db.BooleanProperty()	
	Film = db.BooleanProperty()	
	Repeat = db.BooleanProperty()	
	Subtitles = db.BooleanProperty()	
	Widescreen = db.BooleanProperty()	
	NewSeries = db.BooleanProperty()	
	DeafSigned = db.BooleanProperty()	
	BlackAndWhite = db.BooleanProperty()	
	FilmStars = db.StringProperty()
	FilmCertificate = db.StringProperty()
	Genre = db.StringProperty()
	Description = db.StringProperty()
	RadioTimesChoice = db.StringProperty()
	Date = db.DateTimeProperty()
	StartTime = db.DateTimeProperty() 
	EndTime = db.DateTimeProperty()
	Duration = db.StringProperty()


		
application = webapp.WSGIApplication(
                                     [('/cron/channels', MainPage)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()