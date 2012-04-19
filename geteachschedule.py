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
		# Grabs the next unchecked channel from the datastore and checks it
		# Profiles at just over *** second
		#-------------------------------------------------------------------

		q = db.GqlQuery("SELECT * FROM ChannelInformation WHERE channelchecked = False")
		results = q.fetch(1)
		hello = False
		for entry in results:
			strchannelname = entry.channelname			
			strchannelnumber = entry.channelnumber
			entry.delete()			
			channellisting = ChannelInformation(channelnumber=strchannelnumber, channelname=strchannelname, channelchecked=True)
			channellisting.put()
			self.response.out.write("<br />" + strchannelnumber + " - " + strchannelname)
			q = db.GqlQuery("SELECT * FROM ProgrammeInformation WHERE ChannelNumber = " + strchannelnumber)
			schedule = q.fetch(800)		
			for prog in schedule:
				prog.delete()
			self.response.out.write(examinefile(strchannelnumber, strchannelname))
			hello = True
		if hello == False :
			self.response.out.write("<h1>DONE</h1>")
		
		end = datetime.datetime.now() 
		tdelta = end - start
		self.response.out.write("<br />Ending at " + end.isoformat())
		self.response.out.write("<br />--------<br />Time taken " + str(tdelta))
		
		self.response.out.write('<META HTTP-EQUIV="Refresh" CONTENT="10; URL="/cron/schedule">')

def ParseEntry(entry):
		if entry=="false":
			return False
		else :
			return True
	
# ----------------------------------------------------
# Check through the dat file for each channel
# ----------------------------------------------------	
def examinefile(strChannelNumber, strChannelName):		
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
	for programme in programmes:
	
		#Only do this bit if the series is already mentioned in the database!			
		# ----------------------------------------------------
		# TO DO: only add this entry if the series has a corresponding 
		# match in the series search
		# ----------------------------------------------------	
		detail = programme.split("~")
	
		proginfo = ProgrammeInformation ( ChannelNumber = strChannelNumber,
			ChannelName = strChannelName,	
			ProgrammeTitle = detail[0].decode('utf-8'),
			SubTitle = detail[1].decode('utf-8'),
			Episode = detail[2].decode('utf-8'),
			#Year = detail[3],
			#Director = detail[4],
			#Cast = detail[5],
			#Premiere = ParseEntry(detail[6])	,
			#Film = ParseEntry(detail[7])	,
			#Repeat = ParseEntry(detail[8])	,	
			#Subtitles = ParseEntry(detail[9])	,	
			#Widescreen = ParseEntry(detail[10])	,	
			NewSeries = ParseEntry(detail[11])	,
			#DeafSigned = ParseEntry(detail[12])	,
			#BlackAndWhite = ParseEntry(detail[13])	,	
			#FilmStars = detail[14],
			#FilmCertificate = detail[15],
			#Genre = detail[16],
			#Description = detail[17],
			#RadioTimesChoice = detail[18],
			Date = datetime.datetime.strptime(detail[19], "%d/%m/%Y"),
			StartTime = datetime.datetime.strptime(detail[20], "%H:%M"),
			EndTime = datetime.datetime.strptime(detail[21], "%H:%M"),
			Duration = detail[22].decode('utf-8'))
		proginfo.put()
		
		strReturn +=("<br />written " + detail[0].decode('utf-8') + " = " + detail[21].decode('utf-8') + " = " + detail[20].decode('utf-8'))
	return strReturn	



	
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
                                     [('/cron/schedule', MainPage)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()