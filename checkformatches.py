import urllib
import os
import cgi
import datetime
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from google.appengine.ext import db
from google.appengine.api import mail
from google.appengine.api import datastore_types

	
# ----------------------------------------------------
# TO DO: Redo this so it searches the DB 
# instead of text files. 
# ----------------------------------------------------	

class MainPage(webapp.RequestHandler):
    def get(self):
		self.response.out.write("Starting .. ")
		emailstring = ""
		emailaddress = ""
		# ----------- Find each notification ---------------
		q = db.GqlQuery("SELECT * FROM SeriesSearch ORDER BY emailto ASC")
		results = q.fetch(100)		
		for notification in results:
			# ----------- Send each notification to a function for processing ---------------
			emailstring = CheckForAMatch(notification.seriesname, notification.channels)
			emailaddress = notification.emailto
			self.response.out.write("<br /> checking " + emailaddress + " and " + notification.seriesname )
			if len(emailstring) > 3 :				
				#self.response.out.write('<br />At this point I can send out the following email to ' + emailaddress + "<br />" + emailstring)
				#SendEmail(emailaddress, emailstring)
				message = mail.EmailMessage(sender="amanda.owen@gmail.com",
                            subject="Television Notifier - new series found")				
				message.to = emailaddress
				message.body = emailstring
				message.send()
				self.response.out.write("\n - sent email")
				#now delete the entry from the data store
				notification.delete()
		self.response.out.write("\n<br />DONE")
		

def SendEmail(emailaddress, emailstring):
	message = mail.EmailMessage(sender="Television Notification <televisionnotifier@appspot.gserviceaccount.com>",
                            subject="Television Notifier - new series found")
	#message = mail.EmailMessage(sender="amanda.owen@gmail.com",
    #                        subject="Television Notifier - new series found")
	message.to = emailaddress
	message.body = emailstring
	message.send()

#--------------------------------
# Check a series for a match
#--------------------------------
def CheckForAMatch(seriesname, channels):
	channel = channels.split("#")
	channelnumber = ""
	foundseries = False
	emailstring = ""
	for singlechannel in channel:
		if len(singlechannel) > 2: 
			detail = singlechannel.split("|")
			channelnumber = detail[1]
			channelname = detail[0]
			seriesdatetime = SeriesFound(channelnumber, seriesname)
			if len(seriesdatetime) > 2:
				foundseries = True
				emailstring += "\n" + seriesname + ": " + channelname + " - " + seriesdatetime
	if foundseries == True:
		emailstring = "Found the following new series of " + seriesname + " staring soon. \n" + emailstring
	return emailstring		
		
		
def SeriesFound(channelnumber, series):		
	send = ""
	#Re do this to grab the channel schedule from the datastore
	q = db.GqlQuery("SELECT * FROM SeriesSearch WHERE ChannelNumber = :channel AND ProgrammeTitle = :title AND NewSeries=True", channel=channelnumber, title=series)
	results = q.fetch(1)	
	for entry in results
		send = "found one"
	return send

	
class SeriesSearch(db.Model):
	channels = db.StringProperty()
	seriesname = db.StringProperty()
	emailto = db.StringProperty()
	
class ChannelInformation(db.Model):
	channelnumber = db.StringProperty()
	channelname = db.StringProperty()	
	channelchecked = db.BooleanProperty()		
	
class ProgrammeInformation(db.Model):
	
	ChannelNumber = db.StringProperty()
	ChannelName = db.StringProperty()	
	ProgrammeTitle = db.Text()
	SubTitle = db.Text()
	Episode = db.Text()
	#Year = db.StringProperty()
	#Director = db.StringProperty()
	#Cast = db.StringProperty()
	#Premiere = db.BooleanProperty()	
	#Film = db.BooleanProperty()	
	#Repeat = db.BooleanProperty()	
	#Subtitles = db.BooleanProperty()	
	#Widescreen = db.BooleanProperty()	
	NewSeries = db.BooleanProperty()	
	#DeafSigned = db.BooleanProperty()	
	#BlackAndWhite = db.BooleanProperty()	
	#FilmStars = db.StringProperty()
	#FilmCertificate = db.StringProperty()
	#Genre = db.StringProperty()
	#Description = db.StringProperty()
	#RadioTimesChoice = db.StringProperty()
	Date = db.DateTimeProperty()
	StartTime = db.DateTimeProperty() 
	EndTime = db.DateTimeProperty()
	Duration = db.Text()

		
		
application = webapp.WSGIApplication(
                                     [('/check', MainPage)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()