import urllib
import os
import cgi
import datetime
import commonstrings
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from google.appengine.ext import db

class MainPage(webapp.RequestHandler):
    def post(self):	
	
		user = users.get_current_user()
		if user:		
			applicationname = commonstrings.ApplicationName()
			title = "Email notification has been set"
			description = "An email will be sent to " + user.email() + " when a new series of you selected programme is due to be shown on one of the channels you selected" 
			instructions = "An email will be sent to <b>" + user.email() + "</b> when a new series of you selected programme is due to be shown on one of the channels you selected. Below you can see a list of all the notifications you currently have set. Notifications will be deleted from this system once an email has been sent. " 
			prehtmlcontent = ""
		
			channelstring  = ""
			series = self.request.get("series")
			selectedchannels = self.request.get_all("channels")
			for channel in selectedchannels:
				channelstring += channel + "#"
		
		
			# Use the series search class below to make an entry: 
			seriessearch = SeriesSearch(channels=channelstring, seriesname=series, emailto=user.email())
			seriessearch.put()
		
			prehtmlcontent = GetExistingSearches(user.email())

			#Add all this to the template
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

# ----------------------------------------------------
# Define each set of channels here
# ----------------------------------------------------
def	GetExistingSearches(useremail):
	returnstring = ""
	tablerows = ""
	# The GqlQuery interface constructs a query using a GQL query string.
	q = db.GqlQuery("SELECT * FROM SeriesSearch " +
                "WHERE emailto = :1 " + 
                "ORDER BY emailto ASC",
                useremail)

	# The query is not executed until results are accessed.
	results = q.fetch(100)
	for notification in results:
		#print "%s %s, %d inches tall" % (p.first_name, p.last_name, p.height)
		channels = notification.channels
		channel = channels.split("#")
		channel.remove('')
		channelstring = ("<ul>\n")
		for singlechannel in channel:
			detail = singlechannel.split("|")
			channelstring += ("	<li>" + detail[0] +  "</li>\n")
		channelstring += ("</ul>\n")
		tablerows += "\n\t<tr>\n\t\t<td> %s </td>\n\t\t<td> %s </td>" % (notification.seriesname, channelstring)
		
			
		
	#if len(tablerows) > 2 :
	returnstring = "\n<table  class='table table-striped'>\n\t<tr>\n\t\t<th>Series name</th>\n\t\t<th>Channels</th>\n\t</tr>" + tablerows + "\n</table>" + useremail
	#else:
	#returnstring = "nothing found" 
	return returnstring
		


# ----------------------------------------------------
# Set up the data
# ----------------------------------------------------
class SeriesSearch(db.Model):
	channels = db.StringProperty()
	seriesname = db.StringProperty()
	emailto = db.StringProperty()
	
	
			
application = webapp.WSGIApplication(
                                     [('/setupemail', MainPage)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()