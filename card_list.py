import urllib2
import re
from bs4 import BeautifulSoup

start = 'manual-data-link" href="/'
end = 'data-id='

opener = urllib2.urlopen('https://www.hearthpwn.com/cards/minion?display=1&filter-premium=1')
reader = str(opener.read())
#clean = str(BeautifulSoup(reader,'html.parser'))

search = re.search(r'%s[\a-z|\s|A-Z]+%s' % (start,end),reader)
if search:
	print '%s' % (search.group(0))
else:
	print "error"
#print reader