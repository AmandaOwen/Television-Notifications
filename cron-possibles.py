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
    def get(self, channel):	
		start = datetime.datetime.now()
		self.response.out.write("Starting at " + start.isoformat())
		
		
		#-------------------------------------------------------------------
		# TODO:
		# This should be called with a query string. 
		# Check for ?channel=n
		# Search that channels dat file for all possible matches
		# Write matches to datastore for the next part of the gig
		#-------------------------------------------------------------------
		allprogrammes = []
		allseries = []
	
		q = db.GqlQuery("SELECT * FROM ChannelsToCheck WHERE channelnumber = :channelno", channelno=channel )
		self.response.out.write("<br />Looking at _" + channel)
		results = q.fetch(10)		
		for entry in results:
			#So the channel is one to be found, so we'll do the processing
			self.response.out.write("<br />Found")
			allprogrammes = GetAllProgrammesOnChannel(channel)
			#entry.delete()
		
		q = db.GqlQuery("SELECT * FROM SeriesToCheck" )
		results = q.fetch(200)		
		for entry in results: 
			allseries.append(entry.seriesname.lower())
		
		for programme in allprogrammes: 
			self.response.out.write(programme + "<br />")
			details = programme.split('~')
			if details[0] in allseries: 
				#Put it in the PossiblesToCheck datastore				
				possiblestocheck = PossiblesToCheck(
					ChannelNumber=channel, 
					SeriesName=details[0].encode('utf-8'), 
					Episode=details[1].decode('utf-8'), 
					NewSeries = commonstrings.ParseEntry(details[11]), 
					Date = datetime.datetime.strptime(details[19], "%d/%m/%Y"), 	
					StartTime = datetime.datetime.strptime(details[20], "%H:%M")
				)
				possiblestocheck.put()
		
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
class PossiblesToCheck(db.Model):
	ChannelNumber = db.StringProperty()
	SeriesName = db.TextProperty()
	SubTitle = db.TextProperty()
	Episode = db.TextProperty()	
	NewSeries = db.BooleanProperty()	
	Date = db.DateTimeProperty()
	StartTime = db.DateTimeProperty() 
	
# ----------------------------------------------------
# Check through the dat file for each channel
# ----------------------------------------------------	
def GetAllProgrammesOnChannel(strChannelNumber):		
	#Grab the channel file from the Radio Times
	f = urllib.urlopen("http://xmltv.radiotimes.com/xmltv/" + strChannelNumber + ".dat")		
	s = f.read()
	f.close()
	s = s.lower()
	strReturn = ""
	listofprogrammes = ""
	#Array up the data, and remove the non-programme entries
	programmes = s.split('\n')
	programmes.remove(programmes[0])
	programmes.remove(programmes[0])
	programmes.remove('')	
	return programmes	

		
application = webapp.WSGIApplication(
                                     [('/cron/possibles/(.*)', MainPage)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()