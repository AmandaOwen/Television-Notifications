import urllib
import os
import cgi
import datetime
import commonstrings
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template

class MainPage(webapp.RequestHandler):
    def post(self):	
	
		user = users.get_current_user()
		if user:		
			applicationname = commonstrings.ApplicationName()
			title = "Results of your series search"
			description = "The result of the series search"
			instructions = "Below are all the new series showing on your selected channels."
			formaction = '/setupemail'		
			formcontent = ""
			prehtmlcontent = ""
			channels = commonstrings.GetChannelInformation()	
			
			
			#check if a channel has been selected
			selectedchannels = self.request.get_all("channels")
			series = self.request.get("series")
			foundseries = 0			
			columnlength = len(selectedchannels) / 4
			currentlength = 0
		
			if len(series) < 2 :
				series = ""
			
			#If we're looking for any new series, make sure all the channels get listed
			if len(series) < 2 :
				for channel in selectedchannels:			
					currentlength = currentlength + 1
					detail = channel.split("|")
					if currentlength == 1:
						prehtmlcontent +="\n<div  class='span3'>"
					resultofsearch = examinefile(detail[1], series)
					prehtmlcontent +="\n	<div class='alert'><h2>" + detail[0] + "</h2>"
					if len(resultofsearch) < 2: 
						resultofsearch = "\n			<p>No new series found</p>"
					prehtmlcontent += resultofsearch
					prehtmlcontent += "\n	</div>"
					if currentlength > columnlength: 
						prehtmlcontent += "\n</div>"
						currentlength = 0
				prehtmlcontent += "\n</div>"	
			#If we're looking for a specific series, only list the channels that are showing it, if any
			else :		
				for channel in selectedchannels:
					currentlength = currentlength + 1
					detail = channel.split("|")
					formcontent += ("<input type='hidden' name='channels' id='" + detail[1] + "' value='" + detail[0] + "|" + detail[1] + "' />")
					resultofsearch = examinefile(detail[1], series)
					if len(resultofsearch) > 2: 
						prehtmlcontent +="\n	<div class='alert alert-success'><h2>" + detail[0] + "</h2>"					
						prehtmlcontent += resultofsearch
						prehtmlcontent += "\n	</div>"
						foundseries = 1
				if foundseries == 0: 
					if len(series) > 2 :
						prehtmlcontent = "<div class='alert'><h2>A new series of <em>" + series + "</em> was not found </h2> <p>Would you like to recieve an email when it is about to be shown?</p>\n</div>" 
						formcontent += "<input type='hidden' name ='series' id='series' value='" + series + "' />"
						formcontent += "<input class='btn' type='submit' value='Set up an email alert'>"
						formaction = "/setupemail"
						instructions = "Could not find an episode of your chosen series. You can set an alert: this will email you at " + user.email() + " if a new seres is due to be shown soon."
					else:
						formcontent = ""
						formaction = ""
				else:
					formcontent = ""
					formaction = ""		
		


			#Add all this to the template
			template_values = {
				'title': title,
				'instructions': instructions,
				'applicationname': applicationname,
				'description': description,
				'author': commonstrings.Author(),
				'prehtmlcontent': prehtmlcontent,
				'formcontent': formcontent,
				'formaction': formaction,			
				'username': user.email(),	
				'logouturl': users.create_logout_url(self.request.uri)	
			}
			path = os.path.join(os.path.dirname(__file__), 'index.html')
			self.response.out.write(template.render(path, template_values))	

		else: 
			self.redirect(users.create_login_url(self.request.uri))

# ----------------------------------------------------
# Check through the dat file for each channel to
# match against the series name
# TODO: the "fuzzy" matching C mentioned
# ----------------------------------------------------	
def examinefile(channelnumber, series):		
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
		if len(series) > 0:
			if series.lower() == detail[0]:
				if detail[11] == "true":
					listofprogrammes += ("	<li><strong style='text-transform:capitalize'>" + detail[0] +  "</strong> - " + detail[1] + ": " + detail[19] + " (" + detail[20] + ") </li>\n")
		else:
			if detail[11] == "true" :
				listofprogrammes += ("	<li><strong style='text-transform:capitalize'>" + detail[0] +  "</strong> - " + detail[1] + ": " + detail[19] + " (" + detail[20] + ") </li>\n")
	if len(listofprogrammes) < 3:
		listofprogrammes = ""
	else:
		listofprogrammes = ("\n		<ul>\n" + listofprogrammes + "\n		</ul>")
	return listofprogrammes


			
application = webapp.WSGIApplication(
                                     [('/show', MainPage)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()