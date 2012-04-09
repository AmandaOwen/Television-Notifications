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
		self.response.out.write(""" <table style=\"border:1px solid #f00\"> """)
		for channel in channels:
			details = channel.split("|")						
			self.response.out.write("<tr><td>" + details[0] + "</td><td>" + details[1] + "</td></tr>") 				
		self.response.out.write(""" <table> """)
		self.response.out.write("""
            </body>
          </html>""")

application = webapp.WSGIApplication(
                                     [('/', MainPage)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()