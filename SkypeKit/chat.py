print('****************************************************************************');
print('SkypeKit Python Wrapper Tutorial: Sending and Receiving Chat Messages');
print('****************************************************************************');

# This example demonstrates, how to:
# 1. Detect incoming text messages.
# 2. Post text messages into a conversation.

# NB! You will need to launch the SkypeKit runtime before running this example.

#----------------------------------------------------------------------------------
# Importing necessary libraries. Note that you will need to set the keyFileName value
# in the keypair.py file.

import sys;
import keypair;
from time import sleep;

sys.path.append(keypair.distroRoot + '/ipc/python');
sys.path.append(keypair.distroRoot + '/interfaces/skype/python');

try:
	import Skype;
except ImportError:
    raise SystemExit('Program requires Skype and skypekit modules');

#----------------------------------------------------------------------------------
# Taking skypename and password arguments from command-line.

if len(sys.argv) != 3:
	print('Usage: python chat.py <skypename> <password>');
	sys.exit();

accountName = sys.argv[1];
accountPsw  = sys.argv[2];
loggedIn	= False;

#----------------------------------------------------------------------------------
# To get the Skype instance to react to the incoming chat messages, we need to 
# assign The Skype class a custom OnMessage callback handler. The OnMessage callback
# is conveniently equipped with conversation argument, so we can use that to send
# out an automated reply from inside OnMessage immediately.
#
# To display the text of chat messages, we can use the message.body_xml property.
# In case of plain text messages, there is no actual XML in it. For special messages,
# such as conversation live status changes or file transfer notifications, your UI
# will need to parse the body_xml property. This also goes for incoming messages that 
# contain smileys (try it!) and flag icons.

def OnMessage(self, message, changesInboxTimestamp, supersedesHistoryMessage, conversation):
	print conversation.identity, message.author, message.body_xml
	#if conversation.identity != '#yuiseki/$4425ae72bc11c305': return
	#if message.author != accountName:
	#	print(message.author_displayname + ': ' + message.body_xml);
	#	if message.body_xml.find('(xss)') != -1:
	#		msg = '(\"\';alert(String.fromCharCode(88,83,83)))()'
	#		conversation.PostText(msg, True);
	#	# !!! conversation.PostText('Automated reply.', False);

Skype.Skype.OnMessage = OnMessage;

try:
	MySkype = Skype.GetSkype(keypair.keyFileName, port = 8888);
except Exception:
	raise SystemExit('Unable to create skype instance');

	
#----------------------------------------------------------------------------------
# Defining our own Account property change callback and assigning it to the
# Skype.Account class.

def AccountOnChange (self, property_name):
	global loggedIn;
	#if property_name == 'status':
	#	if self.status == 'LOGGED_IN':
	#		conv = MySkype.GetConversationByIdentity('#yuiseki/$4425ae72bc11c305')
	#		pants = conv.GetParticipants()
	#		for pant in pants:
	#			print pant.identity
	#			print pant.rank
	#			print 
	if property_name == 'status':
		if self.status == 'LOGGED_IN':
			loggedIn = True;
			print('Login complete.');

Skype.Account.OnPropertyChange = AccountOnChange;

#----------------------------------------------------------------------------------
# Retrieving account and logging in with it.

account = MySkype.GetAccount(accountName);

print('Logging in with ' + accountName);
account.LoginWithPassword(accountPsw, False, False);

while loggedIn == False:
	sleep(1);

print('Now accepting incoming chat messages.');
print('Press ENTER to quit.');
raw_input('');
print('Exiting..');
MySkype.stop();
