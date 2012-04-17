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
			formaction = '/setemail'		
			formcontent = ""
			prehtmlcontent = ""
			channels = commonstrings.GetChannelInformation()	
		


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


			
application = webapp.WSGIApplication(
                                     [('/show', MainPage)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()