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
    def get(self):	
	
		user = users.get_current_user()
		if user:		
			applicationname = commonstrings.ApplicationName()
			title = "Choose channels to check"
			description = "Select which series you would like to look out for"
			instructions = "Check the channels you have selected. Then enter a series name, and check for an upcoming new series. You'll be able to set a notifiation if a new series isn't yet scheduled. If you leave the series blank then you'll be able to see all new series showing on your selected channels."
			formaction = '/confirmchannels'		
			channels = commonstrings.GetChannelInformation()				
			startaccordian = commonstrings.StartAccordion()
			middleaccordian = commonstrins.MiddleAccordion()

			#Set up a dictionary
			dictChannels = {}
			for channel in channels: 
				details = channel.split("|")	
				dictChannels[details[0]] =  details[1]
			selectedchannels = self.request.get_all("channels")
			
			
			#setting up the form
			formcontent = ""

			
			#----------------------------
			#Add new stuff here
			#----------------------------
			
			
			
			
			
			#Add all this to the template
			template_values = {
				'title': title,
				'instructions': instructions,
				'applicationname': applicationname,
				'description': description,
				'author': commonstrings.Author(),
				'prehtmlcontent': "",
				'formcontent': formcontent,	
				'formaction': formaction,			
			}
			path = os.path.join(os.path.dirname(__file__), 'index.html')
			self.response.out.write(template.render(path, template_values))
		else: 
			self.redirect(users.create_login_url(self.request.uri))
	
application = webapp.WSGIApplication(
                                     [('/select', MainPage)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()