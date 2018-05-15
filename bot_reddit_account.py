# -*- coding: utf-8 -*-
import praw
import secret
reddit = praw.Reddit(client_id=secret.client_id, client_secret = secret.secret_id, user_agent = secret.user_agent, username = secret.username, password = secret.password)

subreddit = reddit.subreddit('test')
print reddit.read_only

comments = subreddit.stream.comments()
for comment in comments:
	text = comment.body
	text = text.encode('utf-8','ignore')
	print text

#for submission in reddit.subreddit('dota2').hot(limit=1):
#    for submission.	comments.body in submission.comments.list():
#    	print submission.comments.body


#print subreddit.display_name
#print subreddit.title      
#print subreddit.description.encode('utf-8')