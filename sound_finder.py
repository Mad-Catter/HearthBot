import urllib2
import re
from bs4 import BeautifulSoup
#This is where the actual sound is found from the site hearthhead.


#SoundFinder finds the actual sound link from the link of the hearthhead page of a card.  All it needs is the link to the card page and the event in which the sound gets played.
#The events are: being played, attacking, dying, or having a special trigger go off.
def SoundFinder(link, event):
	#Clean is the link given to SoundFinder opened with urllib2, read to make it more accessable to BeautifulSoup, and then cleaned with BeautifulSoup to remove any unwanted code.
	clean = str(BeautifulSoup(urllib2.urlopen(link).read(),'html.parser'))
	#I use regular expressions to find the sound link on the page.  Remove keeps track of how many characters need to be removed from the sound link found.
	#See card_list for my horrendous explanation of regular expressions.
	remove = 20
	#The search terms for the regular expression change with which event is being searched for.  Start is where the search term is being kept.
	#Remove is changed to match the amount of characters for each search termm
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
		sound_link = found[remove:len(found)]
		#Found is the link + the search terms, while sound_link is purely the link to the sound.
		return "http://media.services.zam.com/v1/media/byName/%s" % (sound_link)


def HeroFinder(link,hero_list):
	clean = str(BeautifulSoup(urllib2.urlopen(link).read(),'html.parser'))
	remove=20
	start = 'DEATH_SOUND","url"'
	findall = re.findall(r'%s[\a-z|\s|A-Z]+.ogg' % (start),clean)
	if findall:
		for entry in findall:
			found = entry
			to_be_added = 'http://media.services.zam.com/v1/media/byName/%s' % (found[remove:len(found)])
			hero_list.append(to_be_added)

	start = 'PLAY_SOUND","url"'
	remove = 19
	findall = re.findall(r'%s[\a-z|\s|A-Z]+.ogg' % (start),clean)
	if findall:
		for entry in findall:
			found = entry
			to_be_added = 'http://media.services.zam.com/v1/media/byName/%s' % (found[remove:len(found)])
			hero_list.append(to_be_added)
	
	start = 'ATTACK_SOUND","url"'
	remove = 21
	findall = re.findall(r'%s[\a-z|\s|A-Z]+.ogg' % (start),clean)
	if findall:
		for entry in findall:
			found = entry
			to_be_added = 'http://media.services.zam.com/v1/media/byName/%s' % (found[remove:len(found)])
			hero_list.append(to_be_added)
	

	start = 'OTHER_SOUND","url"'
	remove=20
	findall = re.findall(r'%s[\a-z|\s|A-Z]+.ogg' % (start),clean)
	if findall:
		for entry in findall:
			found = entry
			to_be_added = 'http://media.services.zam.com/v1/media/byName/%s' % (found[remove:len(found)])
			hero_list.append(to_be_added)
	print hero_list
#guldan = []
#HeroFinder('http://www.hearthhead.com/cards/hagatha-the-witch', guldan)
	