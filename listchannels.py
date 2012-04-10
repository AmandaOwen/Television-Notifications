import urllib
import os
import cgi
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template

class MainPage(webapp.RequestHandler):
    def get(self):
		#Grab the channel file from the Radio Times
		f = urllib.urlopen("http://xmltv.radiotimes.com/xmltv/channels.dat")		
		s = f.read()
		f.close()
		
		#Assign the freeview channels
		freeview = ['Channel 4 HD', 'BBC1', 'BBC1 HD', 'BBC2', 'BBC3', 'BBC4', 'BBC News', 'BBC HD', 'CBBC', 'CBeebies', 'Channel 4', 
			'More4', 'Film4', 'E4', '4Music', 'Channel 5', 'Channel 5 HD', '5*', '5USA', 'ITV1', 'ITV2', 'ITV3', 'ITV4', 'ITV1 HD', 
			'CITV', 'S4C', 'Quest', 'Yesterday', 'Challenge', 'Pick TV', 'Dave', 'BBC News', 'BBC Parliament', 'Sky News', 'Al Jazeera English']
		
		#Array up the data, and remove the non-channel entries
		channels = s.split('\n')
		channels.remove(channels[0])
		channels.remove(channels[0])
		channels.remove('')
		
		sortingchannels = ['']
		for channel in channels: 
			details = channel.split("|")	
			sortingchannels.append(details[1] + "|" + details[0])
		channels = sortingchannels
		channels.remove('')
		channels.sort()
		
		#Add the channels to a table with checkboxes
		formcontent = ("<p><a href='#' class='btn btn-info' onClick='SelectFreeview()'>Select Freeview channels</a> or <a href='#'  class='btn btn-info' onClick='Unselect()'>Unselect all</a>\n")		
		formcontent += ("<input type='submit' value='Select channels' class='btn' /> </p>")
		formcontent += ("	<table class='table table-striped'>\n")			
		formcontent += ("		<tbody>\n")
		formcontent += ("		<tr><th>Select?</th><th>Channel name</th>\n")
		for channel in channels:
			details = channel.split("|")						
			formcontent += ("		<tr><td>\n")
			formcontent += ("			<input type='checkbox' name='channels' id='" + details[1] + "' value='" + details[1] + "'")
			if details[0] in freeview: 
				formcontent += (" class='normal freeview' ")
			else:
				formcontent += (" class='normal' ")	
			formcontent += ("/>\n")
			formcontent += ("		</td><td>\n")
			formcontent += ("			<label for='" + details[1] + "'>" + details[0] + "</label>\n")
			formcontent += ("		</td></tr>\n")	
		formcontent += ("		</tbody>\n")
		formcontent += (" </table> ")		
		formcontent += ("<input type='submit' value='Select channels' class='btn' />")
		
		#set up the form to go to the next page
		formaction = '/confirmchannels'
		
	
		#Add all this to the template
		template_values = {
            'title': "Choose the TV channels to scan ",
			'applicationname': "Television Notifications",
			'instructions': "Please select the TV channels you'd like to scan",
            'description': "description",
            'author': "Me!",
			'formcontent': formcontent,
			'formaction': formaction,
        }
		path = os.path.join(os.path.dirname(__file__), 'index.html')
		self.response.out.write(template.render(path, template_values))

class ConfirmChannels(webapp.RequestHandler):
    def post(self):
		#Grab the channel file from the Radio Times
		f = urllib.urlopen("http://xmltv.radiotimes.com/xmltv/channels.dat")		
		s = f.read()
		f.close()
		
		#Array up the data, and remove the non-channel entries
		channels = s.split('\n')
		channels.remove(channels[0])
		channels.remove(channels[0])
		channels.remove('')
		
		dictChannels = {}
		for channel in channels: 
			details = channel.split("|")	
			dictChannels[details[0]] =  details[1]
		selectedchannels = self.request.get_all("channels")
		prehtmlcontent = "\n"
		formcontent = "\n"
		formaction = "/searchshow"
		
		#Show the whole caboodle
		if len(selectedchannels) > 0:
			prehtmlcontent += ("<div class='alert alert-success'><a class='close' data-dismiss='alert'>x</a><p>You have selected "+ str(len(selectedchannels)) + " channels to be scanned.</p>\n")
			prehtmlcontent += ("<ul>\n")
			for channel in selectedchannels:
				prehtmlcontent += ("	<li>" + dictChannels[channel] + " - " + channel +  "</li>\n")
				formcontent += ("<input type='hidden' name='channels' id='" + channel + "' value='" + dictChannels[channel] + "' />")
			prehtmlcontent += ("</ul>\n")
			prehtmlcontent += ("</div>\n")
			formcontent += "<label>Search for: </label><input type='text' class='span3' placeholder='New girl'>"
			formcontent += ("<input type='submit' value='Search' class='btn' />")			
			
		#Add all this to the template
		template_values = {
            'title': "Confirm the TV channels and name a series ",
			'instructions': "Check the correct channels have been selected, and then enter the name of a series you would like to scan for",
			'applicationname': "Television Notifications",
            'description': "description",
            'author': "Me!",
			'prehtmlcontent': prehtmlcontent,
			'formcontent': formcontent,
			'formaction': formaction,
        }
		path = os.path.join(os.path.dirname(__file__), 'index.html')
		self.response.out.write(template.render(path, template_values))
		
class SearchShow(webapp.RequestHandler):
    def post(self):
		selectedchannels = self.request.get_all("channels")
		
					
		#Add all this to the template
		template_values = {
            'title': "Searching for series ",
			'instructions': "Check the correct channels have been selected, and then enter the name of a series you would like to scan for",
			'applicationname': "Television Notifications",
            'description': "description",
            'author': "Me!",
			'prehtmlcontent': "hello",
        }
		path = os.path.join(os.path.dirname(__file__), 'index.html')
		self.response.out.write(template.render(path, template_values))
		

application = webapp.WSGIApplication(
                                     [('/', MainPage),
									  ('/confirmchannels', ConfirmChannels),									  
									  ('/searchshow', SearchShow)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()