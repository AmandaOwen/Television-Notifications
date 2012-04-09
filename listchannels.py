import urllib

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

class MainPage(webapp.RequestHandler):


    def get(self):	
		f = urllib.urlopen("http://xmltv.radiotimes.com/xmltv/channels.dat")		
		s = f.read()
		f.close()
		
		channels = s.split('\n')
		channels.remove(channels[0])
		channels.remove(channels[0])
		channels.remove('')
		self.response.out.write("<html>" + "\n")
		self.response.out.write("	<head>" + "\n")
		self.response.out.write("		<title>Listing channels </title>" + "\n")
		self.response.out.write("	</head>" + "\n")
		self.response.out.write("	<body>" + "\n")
		self.response.out.write("	<form id='channels' action='confirmchannels.py' method='POST'>" + "\n")
		self.response.out.write("	<table> " + "\n")
		for channel in channels:
			details = channel.split("|")						
			self.response.out.write("		<tr><td>" + "\n")
			self.response.out.write("			<input type='checkbox' name='" + details[0] + "' id='" + details[0] + "' value='" + details[0] + "'  />" + "\n")
			self.response.out.write("		</td><td>" + "\n")
			self.response.out.write("			<label for='" + details[0] + "'>" + details[1] + "</label>" + "\n")
			self.response.out.write("		</td></tr>" + "\n")
		self.response.out.write(""" <table> """)
		self.response.out.write("""
			</form>
           </body>
          </html>""")

application = webapp.WSGIApplication(
                                     [('/', MainPage)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()