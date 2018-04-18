import urllib2
import re
from bs4 import BeautifulSoup

StartUrl ="http://media.services.zam.com/v1/media/byName/"
death = 'DEATH_SOUND","url"'
play = 'PLAY_SOUND","url"'
attack = 'ATTACK_SOUND","url"'
trigger = 'TRIGGER_SOUND","url"'
TestEnd = '.ogg'

def linker(link, end):
	bolvar1 = urllib2.urlopen(link)
	bolvar2 = bolvar1.read()
	bolvar = str(BeautifulSoup(bolvar2,'html.parser'))

	remove = 20
	

	if end == "death":
		letter = death
	elif end == "play":
		letter = play
		remove = 19
	elif end == "attack":
		letter = attack
		remove = 21
	elif end == "trigger":
		letter = trigger
		remove = 22
	search = re.search(r'%s[\a-z|\s|A-Z]+%s' % (letter,TestEnd),bolvar)
	if search:
		found = '%s' % (search.group(0))
		TrueFound = found[remove:len(found)]
		print "%s%s" % (StartUrl,TrueFound)
	else:
		print "Error"
	#print bolvar

linker("http://www.hearthhead.com/cards/nexus-champion-saraad","trigger")