import urllib2
import re
#This program takes links to a minion list on the site hearthpwn, and puts them into a list for programing purposes.

minion_list = []
loop=2
#Minion_list is the list of cardsthat will be imported into varios other parts of the bot.
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
		minion_list.append(match[1:len(match)-3])
	#The first search takes the string version of the link and searches for 'manual-data-link" href="/'.  Then it will add all characters from the string (limits aren't working for some reason) until
	#it meets the last "data-id=".  It was supposed to stop at the first data id, but for some reason it went to the last.
	#Basically the first search isolates the chunk of code where the cards are (between the first manual data link and last data id), but with a bunch of usless extra code too.
	#So the second search(which is actually a finditer) does the heavy lifting in extracting the cards.  The second search adds everything between each - and " d, that isnt a white space or = sign.
	#(\S isn't working for some reason.)  Since each idividual card is surround by a - and " d. Then the first charater and last three characters from the matches are removed (The search terms used in search2).
	#Finally the matches are appended to the minion list, and it repeats until all the cards are added.    
	
#dic_of_multiples = {'kelthuzad': 'kelthuzad-1', 'cthun': 'cthun-1', 'emperor-thaurissan': 'emperor-thaurissan-2', 'majordomo-executus': 'majordomo-executus-2', 'rend-blackhand': 'rend-blackhand-2',
#'chromaggus': 'chromaggus-2', 'nefarian': 'nefarian-7', 'blood-queen-lanathel': 'blood-queen-lanathel-2', 'professor-putricide': 'professor-putricide-1', 'sindragosa': 'sindragosa-4',
#'the-darkness': 'the-darkness-2'}

#for card in minion_list:
#	if card in dic_of_multiples:
#		minion_list[minion_list.index(card)] = dic_of_multiples.get(card)
print minion_list