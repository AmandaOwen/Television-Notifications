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
		# Search the possibilities area and match against the set searches
		# TODO: Expand this to check for a specific series+episode
		#-------------------------------------------------------------------

		listofchannels = commonstrings.GetChannelInformation()
		q = db.GqlQuery("SELECT * FROM SeriesSearch")
		results = q.fetch(100)
		for entry in results:
			#Checking against a specific notification request
			pname = entry.seriesname.lower()
			found = []
			strEmail = ""
			q2 = db.GqlQuery("SELECT * FROM PossiblesToCheck WHERE SeriesName = :sname", sname=pname)
			results2 = q2.fetch(200) 
			for entry2 in results2:	
				#Now checking for series that match that notification
				#TODO: Add a check that this series is actually showing on the user's selected channels
				if entry2.NewSeries == True: 
					#Is this a new series? If so add it to the email
					found.append(entry2.SeriesName + "~" + datetime.datetime.strftime(entry2.StartTime, "%H:%M") + "~" + datetime.datetime.strftime(entry2.Date, "%d/%m/%Y") + "~" + FindChannelName(listofchannels, entry2.ChannelNumber))
					#TODO: Check if this is a specific episode of a series	
			if len(found) > 0: 
				#We've got an email to send!
				for f in found:
					items = f.split("~")					
					strEmail += items[0] + " is showing at " + items[1] + " on " + items[2] + " on  " + items[3] + "\n"
				self.response.out.write(strEmail)
				SendEmail(entry.emailto, strEmail)
				#Since we've sent an email, we should delete this entry from the results
				entry.delete()
			
		
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
	SeriesName = db.StringProperty()
	SubTitle = db.StringProperty()
	Episode = db.TextProperty()	
	NewSeries = db.BooleanProperty()	
	Date = db.DateTimeProperty()
	StartTime = db.DateTimeProperty() 
	
# ----------------------------------------------------
# Send teh email
# ----------------------------------------------------		
def SendEmail(emailaddress, emailstring):
	message = mail.EmailMessage(subject="Television Notifier - new series found")
	message.sender = "amanda.owen@gmail.com"
	message.to = emailaddress
	message.body = emailstring
	message.send()
# ----------------------------------------------------
# Find the channel Name
# ----------------------------------------------------	
def FindChannelName(listofchannels, number): 
	strReturn = ""
	for chan in listofchannels: 
		if ("|" + number) in chan: 
			strReturn = chan.replace("|" + number, " ")
	return strReturn

	
application = webapp.WSGIApplication(
                                     [('/cron/emails', MainPage)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()