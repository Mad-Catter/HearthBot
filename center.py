import urllib2
import re
from bs4 import BeautifulSoup
import card_list
#This is where the actual sound is found from the site hearthhead.
#While most of the card sounds will have to be called by stating the card and type of sound, I plan to have a few famous sounds be called a bit eaiser.  Like the priest wow.
wow = "http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_09_WOW_06.ogg"
MinionName = card_list.minion_list[523]
#The link to any minion in hearthhead is always http://www.hearthhead.com/cards/ followed by the minion's name (without any punctuation or capitalization and with all spaces replaced with -)
cardlink = "http://www.hearthhead.com/cards/%s" % (MinionName)
#SoundFinder finds the actual sound link from the link of the hearthhead page of a card.  All it needs is the link to the card page and the event in which the sound gets played.
#The events are: being played, attacking, dying, or having a special trigger go off.
def SoundFinder(link, event):
	#Clean is the link given to SoundFinder opened with urllib2, read to make it more accessable to BeautifulSoup, and then cleaned with BeautifulSoup to remove any unwanted code.
	clean = str(BeautifulSoup(urllib2.urlopen(link).read(),'html.parser'))
	#I use regular expressions to find the sound link on the page.  Remove keeps track of how many characters need to be removed from the sound link found.  See card_list for a horrendous explanation of regular
	#expressions.
	remove = 20
	#The search terms for the regular expression change with which event is being searched for.  Start is where the search term is being kept.  Remove is changed to match the characters of each search termm
	if event == "death":
		start = 'DEATH_SOUND","url"'
	elif event == "play":
		start = 'PLAY_SOUND","url"'
		remove = 19
	elif event == "attack":
		start = 'ATTACK_SOUND","url"'
		remove = 21
	elif event == "trigger":
		start = 'TRIGGER_SOUND","url"'
		remove = 22
	#The search searches through the cleaned link for the start term determined earlier, and ends once it hits .ogg (something the sound links always end with).
	search = re.search(r'%s[\a-z|\s|A-Z]+.ogg' % (start),clean)
	if search:
		found = '%s' % (search.group(0))
		SoundLink = found[remove:len(found)]
		#Found is the link + the serach terms, while SoundLink is purely the link to the sound.
		print "http://media.services.zam.com/v1/media/byName/%s" % (SoundLink)
		return "http://media.services.zam.com/v1/media/byName/%s" % (SoundLink)

SoundFinder('http://www.hearthhead.com/cards/nexus-champion-saraad',"trigger")
SoundFinder(cardlink,"play")
