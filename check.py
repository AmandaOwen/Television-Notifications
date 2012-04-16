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
	#Grab the channel file from the Radio Times
	f = urllib.urlopen("http://xmltv.radiotimes.com/xmltv/" + channelnumber + ".dat")		
	s = f.read()
	f.close()
	s = s.lower()
	listofprogrammes = ""
	#Array up the data, and remove the non-programme entries
	programmes = s.split('\n')
	programmes.remove(programmes[0])
	programmes.remove(programmes[0])
	programmes.remove('')
	for programme in programmes:
		detail = programme.split("~")
		if series.lower() == detail[0]:
			if detail[11] == "true":
				#then this is a match, and we need to make sure we send an email
				send = detail[19] + " (" + detail[20] + ")"
	return send

	
class SeriesSearch(db.Model):
	channels = db.StringProperty()
	seriesname = db.StringProperty()
	emailto = db.StringProperty()

		
		
application = webapp.WSGIApplication(
                                     [('/check', MainPage)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()