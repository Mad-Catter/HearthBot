import urllib2
import re
#This program takes links to a minion list on the site hearthpwn, and puts them into a list for programing purposes.

minion_list = []
loop=1
#Minion_list is the list of cards that will be imported into various other parts of the bot.
list_of_lists = ['https://www.hearthpwn.com/cards/minion?display=1&filter-premium=1']
#The list of lists contains all of the links to the card list on hearthpwn.  Hearthpwn has all of the cards spread out between differnt links as to not clutter the screen.
while loop < 12:
	loop+=1
	list_of_lists.append('https://www.hearthpwn.com/cards/minion?display=1&filter-premium=1&page=%s' %(loop))
	#The list of lists starts out with one link to the first page, and the rest of the links get added here.  The first link is a bit different from the rest of them, but the rest only differ from eachother
	#by the page number.  So instead of adding them all by hand I made a while loop which just changes the page number each loop.... I am a lazy man.
	#There are currently only 12 links at the time of making this code (Witchwood has just launched).
for link in list_of_lists:
	opener = urllib2.urlopen(link)
	reader = str(opener.read())
	#Opener and reader just takes the link from the list of lists and turns all of its content into a string.

	search = re.search(r'manual-data-link" href="/[\a-z|A-Z|-|\d]+" data-id=',reader)
	if search:
		blines = '%s' % (search.group(0))
	search2 = re.finditer(r'-[^ \t\n\r\f\v\=]+" d' ,blines)
	for match in search2:
		match = "%s" % (match.group(0))
		match = match[1:len(match)-3]
		#match = "((%s))" % (match)
		minion_list.append(match)
	#The first search takes the string version of the link and searches for 'manual-data-link" href="/'.  Then it will add all characters from the string (limits aren't working for some reason) until
	#it meets the last "data-id=".  It was supposed to stop at the first data id, but for some reason it went to the last.
	#Basically the first search isolates the chunk of code where the cards are (between the first manual data link and last data id), but with a bunch of usless extra code too.
	#So the second search(which is actually a finditer) does the heavy lifting in extracting the cards.  The second search adds everything between each - and " d, that isnt a white space or = sign.
	#(\S also isn't working for some reason.)  Since each idividual card is surround by a - and " d.
	#Then the first charater and last three characters from the matches are removed (The search terms used in search2).
	#Finally the matches are appended to the minion list, and it repeats until all the cards are added.

#In hearthstone the 'Death Knight' cards have their own lines, and are worthy of being added to the bot.  However since the cards are not minions they do not get added to the minion list automatically.
#So here they are being added semi-manually.
death_knights = ['shadowreaper-anduin', 'thrall-deathseer', 'frost-lich-jaina', 'scourgelord-garrosh', 'valeera-the-hollow', 'bloodreaver-guldan', 'uther-of-the-ebon-blade', 'malfurion-the-pestilent']
for entry in death_knights:
	minion_list.append(entry)
#The links I use for finding the sounds of the cards use the periods of the cards in their link.
#However periods aren't caught in the automatic search, so the versions without periods are replaced with the versions with periods here.
period_list = ['dr.-boom', 'venture-co.-mercenary']
for entry in period_list:
	minion_list.remove(entry.replace('.',''))
	minion_list.append(entry)

print minion_list