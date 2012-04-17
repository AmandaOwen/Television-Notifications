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
			title = "Choose channels to check"
			description = "Select which series you would like to look out for"
			instructions = "Check the channels you have selected. Then enter a series name, and check for an upcoming new series. You'll be able to set a notifiation if a new series isn't yet scheduled. If you leave the series blank then you'll be able to see all new series showing on your selected channels."
			formaction = '/show'		
			channels = commonstrings.GetChannelInformation()				
			startaccordion = commonstrings.StartAccordion()
			middleaccordion = commonstrings.MiddleAccordion()
			endaccordion = commonstrings.EndAccordion()
			
			
			#check if a channel has been selected
			selectedchannels = self.request.get_all("channels")
			
			if len(selectedchannels) > 0:

				#Set up a dictionary
				dictChannels = {}
				for channel in channels: 
					details = channel.split("|")	
					dictChannels[details[1]] =  details[0]				
				
				#setting up the form (more in loop below)
				formcontent = ""
				#setting up the confirmation area
				prehtmlcontent = ("<ul>\n")
				for channel in selectedchannels:
					#prehtmlcontent += ("	<li>" + channel +  "</li>\n")
					prehtmlcontent += ("	<li>" + dictChannels[channel] + " - " + channel +  "</li>\n")
					formcontent += ("<input type='hidden' name='channels' id='" + channel + "' value='" + dictChannels[channel] + "|" + channel + "' />")
				prehtmlcontent += ("</ul>\n")
				prehtmlcontent = startaccordion + "<p>You have selected " + str(len(selectedchannels)) + " channels to be scanned. <i class='icon-arrow-down'></i></p>\n" + middleaccordion + prehtmlcontent + 	endaccordion				
				formcontent += "<label>Search for: </label><input type='text' class='span3' placeholder='type series name here' name='series' id='series'>"
				formcontent += ("<input type='submit' value='Search' class='btn' />")	
				
				#Add all this to the template
				template_values = {
					'title': title,
					'instructions': instructions,
					'applicationname': applicationname,
					'description': description,
					'author': commonstrings.Author(),
					'prehtmlcontent': "		<div class='span6'>\n" + prehtmlcontent + "				</div>",
					'formcontent': "		<div class='span6'>\n" + formcontent + "				</div>",
					'formaction': formaction,			
					'username': user.email(),	
					'logouturl': users.create_logout_url(self.request.uri)	
				}
				path = os.path.join(os.path.dirname(__file__), 'index.html')
				self.response.out.write(template.render(path, template_values))	
			else :
				#if no channels were selected	
				instructions = "You would normally get to select your series here - but you haven't selected any channels yet!"
				prehtmlcontent = "Please go back to the <a href='/channels'>Channels</a> page to select your channels before attempting this step."

				template_values = {
					'title': title,
					'instructions': instructions,
					'applicationname': applicationname,
					'description': description,
					'author': commonstrings.Author(),
					'prehtmlcontent': prehtmlcontent,		
					'username': user.email(),	
					'logouturl': users.create_logout_url(self.request.uri)	
				}
				path = os.path.join(os.path.dirname(__file__), 'index.html')
				self.response.out.write(template.render(path, template_values))	
			
		else: 
			self.redirect(users.create_login_url(self.request.uri))
	
application = webapp.WSGIApplication(
                                     [('/series', MainPage)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()