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
		
		#Assign the default select buttons/channels
		freeview = GetFreeviewChannels()
		skysports = GetSkySports()
		skyentertainment = GetSkyEntertainment()
		
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
				
		
		#Build the buttons that appear at the top of the form
		
		buttons = ("""    
					<div class="span12">
						<div class="btn-group" style="float:left; padding-right:10px;">
						<a href="#" class="btn" onClick="return false;">Selections...</a>
						<button class="btn dropdown-toggle" data-toggle="dropdown">
						<span class="caret"></span>
						</button>
						<ul class="dropdown-menu">
							<li><a href='#' onClick='SelectType(".freeview"); return false;'>Select Freeview channels</a></li>
							<li><a href='#' onClick='SelectType(".skysports"); return false;'>Select Sky Sports channels</a></li>
							<li><a href='#' onClick='SelectType(".skyentertainment"); return false;'>Select Sky Entertainment channels</a></li>
							<li><a href="#" onClick="Unselect(); return false;">Clear selections</a></li>
						</ul>
						</div>
						<input type='submit' value='Select channels' class='btn' /> <br />
					</div>
		""")
	
		#Add the channels to a table with checkboxes
		#
		formcontent = ("\n")

		#These will help figure out when to start a new div/table, so the content can be compressed into columns
		columnlength = len(channels) / 4
		currentlength = 0
		for channel in channels:
			currentlength = currentlength + 1
			#Start the table if appropriate
			if currentlength == 1:
				formcontent += ("	<div class='span3'><br />")
				formcontent += ("	<table class='table table-striped'>\n")			
				formcontent += ("		<tbody>\n")
				formcontent += ("		<tr><th>Select?</th><th>Channel name</th>\n")
			details = channel.split("|")						
			formcontent += ("		<tr><td>\n")
			formcontent += ("			<input type='checkbox' name='channels' id='" + details[1] + "' value='" + details[1] + "'")
			if details[0] in freeview: 
				formcontent += (" class='normal freeview' ")
			elif details[0] in skysports:
				formcontent += (" class='normal skysports' ")
			elif details[0] in skyentertainment:
				formcontent += (" class='normal skyentertainment' ")
			else:
				formcontent += (" class='normal' ")	
			formcontent += ("/>\n")
			formcontent += ("		</td><td>\n")
			formcontent += ("			<label for='" + details[1] + "'>" + details[0] + "</label>\n")
			formcontent += ("		</td></tr>\n")
			#Now close off the table if appropriate
			if currentlength > columnlength:
				formcontent += ("		</tbody>\n")
				formcontent += (" </table> \n")	
				formcontent += (" </div> \n")	
				currentlength = 0
		
		formcontent += ("		</tbody>\n")
		formcontent += (" </table> \n")	
		formcontent += (" </div> \n")	
		formcontent += ("<div class='span12'><input type='submit' value='Select channels' class='btn' /></div>")
		
		#set up the form to go to the next page
		formaction = '/confirmchannels'
		
	
		#Add all this to the template
		template_values = {
            'title': "Choose the TV channels to scan ",
			'applicationname': "Television Notifications",
			'instructions': "Please select the TV channels you'd like to scan",
            'description': "description",
            'author': "Me!",
			'formcontent': buttons + formcontent,
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
		
		youhaveselectedpre = ("""			
          <div class="accordion" id="accordion2">
            <div class="accordion-group">
              <div class="accordion-heading alert-success">
                <a class="accordion-toggle" data-toggle="collapse" data-parent="#accordion2" href="#collapseOne">
		""")
		youhaveselectedpost = ("""
		 		</a>
             </div>
             <div style="height: 0px;" id="collapseOne" class="accordion-body collapse">
                <div class="accordion-inner alert-success">
        """)
		
		channellistpost = ("""
                </div>
             </div>
        </div>
		</div>
			""")
		
		
		#Show the whole caboodle
		if len(selectedchannels) > 0:
			prehtmlcontent += ("<ul>\n")
			for channel in selectedchannels:
				prehtmlcontent += ("	<li>" + dictChannels[channel] + " - " + channel +  "</li>\n")
				formcontent += ("<input type='hidden' name='channels' id='" + channel + "' value='" + dictChannels[channel] + "|" + channel + "' />")
			prehtmlcontent += ("</ul>\n")
			prehtmlcontent = youhaveselectedpre + "<p>You have selected "+ str(len(selectedchannels)) + " channels to be scanned.</p>\n" + youhaveselectedpost + prehtmlcontent + channellistpost

			
			formcontent += "<label>Search for: </label><input type='text' class='span3' placeholder='New girl' name='series' id='series'>"
			formcontent += ("<input type='submit' value='Search' class='btn' />")			
			
		#Add all this to the template
		template_values = {
            'title': "Confirm the TV channels and name a series ",
			'instructions': "Check the correct channels have been selected, and then enter the name of a series you would like to scan for",
			'applicationname': "Television Notifications",
            'description': "description",
            'author': "Me!",
			'prehtmlcontent': "		<div class='span6'>\n" + prehtmlcontent + "				</div>",
			'formcontent': "		<div class='span6'>\n" + formcontent + "				</div>",
			'formaction': formaction,
        }
		path = os.path.join(os.path.dirname(__file__), 'index.html')
		self.response.out.write(template.render(path, template_values))
		
class SearchShow(webapp.RequestHandler):
    def post(self):
		#test of new function
		#prehtmlcontent = examinefile("92", "")
		
		prehtmlcontent = ""
		selectedchannels = self.request.get_all("channels")
		series = self.request.get("series")
		foundseries = 0
		
		if len(series) < 2 :
			series = ""
		
		#selectedchannels.remove("")
		columnlength = len(selectedchannels) / 4
		currentlength = 0
		
		#If we're looking for any news series, make sure all the channels get listed
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
				resultofsearch = examinefile(detail[1], series)
				if len(resultofsearch) > 2: 
					prehtmlcontent +="\n	<div class='alert alert-success'><h2>" + detail[0] + "</h2>"					
					prehtmlcontent += resultofsearch
					prehtmlcontent += "\n	</div>"
					foundseries = 1
			if foundseries == 0: 
				if len(series) > 2 :
					prehtmlcontent = "<div class='alert'><h2>A new series of <em>" + series + "</em> was not found - would you like to recieve an email when it is about to be shown?</h2>\n" 
		
		
		#Add all this to the template
		template_values = {
            'title': "Searching for series ",
			'instructions': "Scanning...",
			'applicationname': "Television Notifications",
            'description': "description",
            'author': "Me!",
			'prehtmlcontent': prehtmlcontent,
        }
		path = os.path.join(os.path.dirname(__file__), 'index.html')
		self.response.out.write(template.render(path, template_values))
		
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

# ----------------------------------------------------
# Define each set of channels here
# ----------------------------------------------------
def GetFreeviewChannels(): 
	channels = ['Channel 4 HD', 'BBC1', 'BBC1 HD', 'BBC2', 'BBC3', 'BBC4', 'BBC News', 'BBC HD', 'CBBC', 'CBeebies', 'Channel 4', 
			'More4', 'Film4', 'E4', '4Music', 'Channel 5', 'Channel 5 HD', '5*', '5USA', 'ITV1', 'ITV2', 'ITV3', 'ITV4', 'ITV1 HD', 
			'CITV', 'S4C', 'Quest', 'Yesterday', 'Challenge', 'Pick TV', 'Dave', 'BBC News', 'BBC Parliament', 'Sky News', 'Al Jazeera English']
	return channels
def GetSkySports(): 
	channels = ['Sky Sports 1', 'Sky Sports 2', 'Sky Sports 3', 'Sky Sports 4', 'Sky Sports F1', 'Sky Sports News']
	return channels	
def GetSkyEntertainment(): 
	channels = ['Sky Atlantic', 'Sky 1', 'Sky Living', 'Sky Arts 1', 'Sky Arts 2', 'Comedy Central', 'FX']
	return channels	
		
		
application = webapp.WSGIApplication(
                                     [('/', MainPage),
									  ('/confirmchannels', ConfirmChannels),									  
									  ('/searchshow', SearchShow)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()