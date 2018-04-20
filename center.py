import urllib2
import re
from bs4 import BeautifulSoup
import card_list

minion_list = card_list.minion_list

StartUrl ="http://media.services.zam.com/v1/media/byName/"
death = 'DEATH_SOUND","url"'
play = 'PLAY_SOUND","url"'
attack = 'ATTACK_SOUND","url"'
trigger = 'TRIGGER_SOUND","url"'
TestEnd = '.ogg'
wow = "http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_09_WOW_06.ogg"
def linker(link, end):
	opener = urllib2.urlopen(link)
	reader = opener.read()
	clean = str(BeautifulSoup(reader,'html.parser'))
	#print clean
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
	search = re.search(r'%s[\a-z|\s|A-Z]+%s' % (letter,TestEnd),clean)
	if search:
		found = '%s' % (search.group(0))
		TrueFound = found[remove:len(found)]
		print "%s%s" % (StartUrl,TrueFound)
	else:
		print "Error"

linker("http://www.hearthhead.com/cards/nexus-champion-saraad","attack")
