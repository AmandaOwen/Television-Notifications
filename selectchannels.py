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
<<<<<<< HEAD
	
=======
>>>>>>> 510e4e1cd1fe4448b34543515e7da43dc58ca15e
		user = users.get_current_user()
		if user:		
			applicationname = commonstrings.ApplicationName()
			title = "Choose channels to check"
			description = "Select which channels you would like to examine"
			instructions = "Below are UK TV channels, as listed in the Radio Times. Select ones you would like to check, or use the drop down list to select a group. Once you've done this submit the form. On the next page you'll be shown a summary of the channels you've picked, and asked about the series you'd like to check on."
<<<<<<< HEAD
			formaction = '/confirmchannels'		
=======
			formaction = '/series'		
>>>>>>> 510e4e1cd1fe4448b34543515e7da43dc58ca15e
			channels = commonstrings.GetChannelInformation()				
			freeview = commonstrings.GetFreeview()
			skysports = commonstrings.GetSkySports()
			skyentertainment = commonstrings.GetSkyEntertainment()
			
			#setting up the form
			formcontent = commonstrings.SelectChannelButtons()

			#These will help figure out when to start a new div/table, 
			#so the content can be compressed into columns
			columnlength = len(channels) / 4
			currentlength = 0
			for channel in channels:
				currentlength = currentlength + 1
				#Start the table if appropriate
				if currentlength == 1:
					formcontent += commonstrings.GetTableHead()
				details = channel.split("|")						
				formcontent += ("\n\t\t\t\t\t\t\t<tr><td>")
				formcontent += ("\n\t\t\t\t\t\t\t\t<input type='checkbox' name='channels' id='" + details[1] + "' value='" + details[1] + "'")
				if details[0] in freeview: 
					formcontent += (" class='normal freeview' ")
				elif details[0] in skysports:
					formcontent += (" class='normal skysports' ")
				elif details[0] in skyentertainment:
					formcontent += (" class='normal skyentertainment' ")
				else:
					formcontent += (" class='normal' ")	
				formcontent += ("/>")
				formcontent += ("\n\t\t\t\t\t\t\t</td><td>")
				formcontent += ("\n\t\t\t\t\t\t\t<label for='" + details[1] + "'>" + details[0] + "</label>")
				formcontent += ("\n\t\t\t\t\t\t</td></tr>")
				#Now close off the table if appropriate
				if currentlength > columnlength:
					formcontent += commonstrings.GetTableFoot()
					currentlength = 0
			
			formcontent += commonstrings.GetTableFoot()
			formcontent += ("<div class='span12'><input type='submit' value='Select channels' class='btn' /></div>")
			
<<<<<<< HEAD
=======
			
			
>>>>>>> 510e4e1cd1fe4448b34543515e7da43dc58ca15e
			#Add all this to the template
			template_values = {
				'title': title,
				'instructions': instructions,
				'applicationname': applicationname,
				'description': description,
				'author': commonstrings.Author(),
				'prehtmlcontent': "",
				'formcontent': formcontent,	
<<<<<<< HEAD
				'formaction': formaction,			
=======
				'formaction': formaction,	
				'username': user.email(),	
				'logouturl': users.create_logout_url(self.request.uri)	
>>>>>>> 510e4e1cd1fe4448b34543515e7da43dc58ca15e
			}
			path = os.path.join(os.path.dirname(__file__), 'index.html')
			self.response.out.write(template.render(path, template_values))
		else: 
			self.redirect(users.create_login_url(self.request.uri))
	
application = webapp.WSGIApplication(
                                     [('/channels', MainPage)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()