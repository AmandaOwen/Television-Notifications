import urllib
# ----------------------------------------------------
# A place for reusable bits of content so they're 
# easy to find. 
# ----------------------------------------------------

def ApplicationName(): 
	s = "Television Notifier"
	return s
def Author(): 
	return "Amanda Owen"


# ----------------------------------------------------
# Work on the Radio Times dat files
# ----------------------------------------------------	
def GetChannelInformation(): 
	#Find the file
	f = urllib.urlopen("http://xmltv.radiotimes.com/xmltv/channels.dat")		
	s = f.read()
	f.close()	
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
	return channels

# ----------------------------------------------------
# Define each set of channels here
# ----------------------------------------------------
def GetFreeview(): 
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


# ----------------------------------------------------
# Bits and pieces for the form on the first page
# ----------------------------------------------------	
def SelectChannelButtons():
	s = ("""    
	
			<!-- Buttons for form -->
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
			<!-- End Buttons for form -->

			""")
	return s

def GetTableHead():
	s = ("""	
			<div class='span3'><br />
				<table class='table table-striped'>			
					<tbody>
						<tr><th>Select</th><th>Channel name</th></tr>
		""")
	return s
		
def GetTableFoot():
	s = ("""
					</tbody>
				</table>
			</div>
		""")
	return s

# ----------------------------------------------------
# Bits and pieces for the second page
# ----------------------------------------------------	
def StartAccordion():
	s = ("""			
          <div class="accordion" id="accordion2">
            <div class="accordion-group">
              <div class="accordion-heading">
                <a class="accordion-toggle" data-toggle="collapse" data-parent="#accordion2" href="#collapseOne">
		""")
	return s
def MiddleAccordion():
	s = ("""			
		 		</a>
             </div>
             <div style="height: 0px;" id="collapseOne" class="accordion-body collapse">
                <div class="accordion-inner">
		""")
	return s
def EndAccordion():

	s = ("""
                </div>
             </div>
        </div>
		</div>
			""")	
	return s