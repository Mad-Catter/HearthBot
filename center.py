# -*- coding: utf-8 -*-
from sound_finder import SoundFinder
from string import capwords
import os
import praw
import re
from random import randint
import time
#SoundFinder (my own creation) is imported to get the links to the sounds from hearthhead.  capwords is imported from string to capitalize each word of a card name).
#praw is a module made specifically to help people make their own reddit bots... which I am using to make my own reddit bot.  secret holds information for praw which I don't want to pubically share.
#re is imported to better search for cards in comments and randint is imported to create a random number for later.

#This is the suggested setup for praw.  It takes the various ids hidden in secret to log the bot into reddit.
#Then it will use .stream to put the last 100 comments written in a certain subreddit like r/hearthstone into a list.
reddit = praw.Reddit(client_id=os.environ.get('reddit_client_id'), client_secret = os.environ.get('reddit_secret_id'), user_agent = os.environ.get('reddit_user_agent').replace('-',' '), username = os.environ.get('reddit_username'), password = os.environ.get('reddit_password'))
subreddit = reddit.subreddit('test')
comments = subreddit.stream.comments()



special_lines = {'wow':'"http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_09_WOW_06.ogg"',}


#If a card is a boss in the game, they will have two different links on the hearthhead website.  So this is a dictonary of any cards with a differnt link from their name.
dic_of_multiples = {'kelthuzad': 'kelthuzad-1', 'cthun': 'cthun-1', 'emperor-thaurissan': 'emperor-thaurissan-2', 'majordomo-executus': 'majordomo-executus-2', 'rend-blackhand': 'rend-blackhand-2',
'chromaggus': 'chromaggus-2', 'nefarian': 'nefarian-7', 'blood-queen-lanathel': 'blood-queen-lanathel-2', 'professor-putricide': 'professor-putricide-1', 'sindragosa': 'sindragosa-4',
'the-darkness': 'the-darkness-2', 'prince-malchezaar': 'prince-malchezaar-4', 'valeera-the-hollow': 'valeera-the-hollow-1', 'romulo': 'romulo-1', 'frozen-champion': 'frozen-champion-2',
'druid-of-the-swarm': 'druid-of-the-swarm-2', 'dorothee': 'dorothee-1', 'boom-bot': 'boom-bot-1'}


anduin = {'no-mana': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_09_ERROR02_21.ogg', 'no-cards': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_09_NoCards_19.ogg', 'hero-death': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_09_Death_17.ogg', 'concede': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_09_Concede_07.ogg', 'greetings-pirate': 'http://media.services.zam.com/v1/media/byName/hs/sounds/enus/VO_HERO_09_PIRATE_DAY_33.ogg', 'too-many-minions': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_09_ERROR07_26.ogg', 'greetings-halloween': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_09_HAPPY_HALLOWEEN_13.ogg', 'stealth': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_09_ERROR08_27.ogg', 'well-played': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_09_Well%20Played_02.ogg', 'thinking-3': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_09_Thinking3_14.ogg', 'greetings-new-year': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_09_HAPPY_NEW_YEAR_15.ogg', 'hand-full': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_09_ERROR06_25.ogg', 'low-cards': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_09_LowCards_18.ogg', 'need-weapon': 'http://media.services.zam.com/v1/media/byName/hs/sounds/enus/VO_HERO_09_ERROR01_20.ogg', 'sorry': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_09_Sorry_06.ogg', 'taunt': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_09_ERROR11_20.ogg', 'mirror': 'http://media.services.zam.com/v1/media/byName/hs/sounds/enus/VO_HERO_09_MIRROR_START_01.ogg', 'thinking-1': 'http://media.services.zam.com/v1/media/byName/hs/sounds/enus/VO_HERO_09_Thinking1_12.ogg', 'greetings-holidays': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_09_HAPPY_HOLIDAYS_14.ogg', 'thanks': 'http://media.services.zam.com/v1/media/byName/hs/sounds/enus/VO_HERO_09_Thanks_05.ogg', 'generic-error': 'http://media.services.zam.com/v1/media/byName/hs/sounds/enus/VO_HERO_09_ERROR12_31.ogg', 'minion-sleep': 'http://media.services.zam.com/v1/media/byName/hs/sounds/enus/VO_HERO_09_ERROR05_24.ogg', 'picked': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_09_Picked_08.ogg', 'hero-attack': 'http://media.services.zam.com/v1/media/byName/hs/sounds/enus/VO_HERO_09_Attack_16.ogg', 'greetings': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_09_Greetings_01.ogg', 'weapon-ready': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_09_Weapon_10.ogg', 'start': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_09_Start_09.ogg', 'limited-time': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_09_Time_11.ogg', 'minion-attacked': 'http://media.services.zam.com/v1/media/byName/hs/sounds/enus/VO_HERO_09_ERROR03_22.ogg', 'threaten': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_09_Threaten_04.ogg', 'thinking-2': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_09_Thinking2_13.ogg', 'hero-attacked': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_09_ERROR04_23.ogg', 'greetings-fire': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_09_FIRE_FESTIVAL_32.ogg', 'wow': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_09_WOW_06.ogg', 'oops': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_09_Oops_03.ogg', 'invalid-target': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_09_ERROR10_29.ogg', 'cant-play': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_09_ERROR09_28.ogg', 'greetings-noblegarden': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_09_HAPPY_NOBLEGARDEN_17.ogg'}
garrosh = {'cant-play': 'http://media.services.zam.com/v1/media/byName/hs/sounds/enus/VO_HERO_01_ERROR09_28.ogg', 'invalid-target': 'http://media.services.zam.com/v1/media/byName/hs/sounds/enus/VO_HERO_01_ERROR10_29.ogg', 'greetings-holidays': 'http://media.services.zam.com/v1/media/byName/hs/sounds/enus/VO_HERO_01_HAPPY_HOLIDAYS_05.ogg', 'greetings-pirate': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_01_PIRATE_DAY_33.ogg', 'hero-attacked': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_01_ERROR04_23.ogg', 'weapon-ready': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_01_Weapon_10.ogg', 'picked': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_01_Picked_08.ogg', 'taunt': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_01_ERROR11_20.ogg', 'low-cards': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_01_LowCards_18.ogg', 'no-cards': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_01_NoCards_19.ogg', 'wow': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_01_WOW_11.ogg', 'no-mana': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_01_ERROR02_21.ogg', 'thinking-3': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_01_Thinking3_14.ogg', 'thanks': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_01_Thanks_05.ogg', 'start': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_01_Start_09.ogg', 'limited-time': 'http://media.services.zam.com/v1/media/byName/hs/sounds/enus/VO_HERO_01_Time_11.ogg', 'stealth': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_01_ERROR08_27.ogg', 'minion-attacked': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_01_ERROR03_22.ogg', 'thinking-2': 'http://media.services.zam.com/v1/media/byName/hs/sounds/enus/VO_HERO_01_Thinking2_13.ogg', 'greetings-halloween': 'http://media.services.zam.com/v1/media/byName/hs/sounds/enus/VO_HERO_01_HAPPY_HALLOWEEN_04.ogg', 'threaten': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_01_Threaten_04.ogg', 'sorry-2': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_01_Sorry_06_ALT.ogg', 'greetings-new-year': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_01_HAPPY_NEW_YEAR_06.ogg', 'hand-full': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_01_ERROR06_25.ogg', 'need-weapon': 'http://media.services.zam.com/v1/media/byName/hs/sounds/enus/VO_HERO_01_ERROR01_20.ogg', 'thinking-1': 'http://media.services.zam.com/v1/media/byName/hs/sounds/enus/VO_HERO_01_Thinking1_12.ogg', 'oops': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_01_Oops_03.ogg', 'greetings': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_01_Greetings_01.ogg', 'thanks-2': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_01_Thanks_05_ALT.ogg', 'hero-attack': 'http://media.services.zam.com/v1/media/byName/hs/sounds/enus/VO_HERO_01_Attack_16.ogg', 'well-played': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_01_Well%20Played_02.ogg', 'too-many-minions': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_01_ERROR07_26.ogg', 'hero-death': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_01_Death_17.ogg', 'concede': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_01_Concede_07.ogg', 'sorry': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_01_Sorry_06.ogg', 'minion-sleep': 'http://media.services.zam.com/v1/media/byName/hs/sounds/enus/VO_HERO_01_ERROR05_24.ogg', 'mirror': 'http://media.services.zam.com/v1/media/byName/hs/sounds/enus/VO_HERO_01_MIRROR_START_02.ogg', 'generic-error': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_01_ERROR12_31.ogg', 'greetings-fire': 'http://media.services.zam.com/v1/media/byName/hs/sounds/enus/VO_HERO_01_FIRE_FESTIVAL_32.ogg', 'greetings-noblegarden': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_01_HAPPY_NOBLEGARDEN_17.ogg'}
guldan = {'hero-death': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_07_Death_17.ogg', 'well-played': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_07_Well Played_02.ogg', 'hero-attack': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_07_Attack_16.ogg', 'no-cards:': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_07_NoCards_19.ogg', 'greetings-fire': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_07_FIRE_FESTIVAL_32.ogg', 'greetings': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_07_Greetings_01.ogg', 'thinking-3': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_07_Thinking3_14.ogg', 'no-mana': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_07_ERROR02_21.ogg', 'minion-attacked': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_07_ERROR03_22.ogg', 'limited-time': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_07_Time_11.ogg', 'stealth': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_07_ERROR08_27.ogg', 'wow': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_07_WOW_06.ogg', 'cant-play': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_07_ERROR09_28.ogg', 'greetings-holidays': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_07_HAPPY_HOLIDAYS_14.ogg', 'invalid-target': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_07_ERROR10_29.ogg', 'mirror': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_07_MIRROR_START_01.ogg', 'thinking-2': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_07_Thinking2_13.ogg', 'taunt': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_07_ERROR11_20.ogg', 'hero-attacked': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_07_ERROR04_23.ogg', 'threaten': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_07_Threaten_04.ogg', 'oops-2':  'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_07_Oops_03_ALT.ogg', 'weapon-ready': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_07_Weapon_10.ogg', 'minion-sleep': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_07_ERROR05_24.ogg', 'sorry': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_07_Sorry_06.ogg', 'thanks':  'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_07_Thanks_05.ogg', 'greetings-halloween': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_07_HAPPY_HALLOWEEN_13.ogg', 'thinking-1': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_07_Thinking1_12.ogg','low-cards': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_07_LowCards_18.ogg', 'generic-error': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_07_ERROR12_31.ogg', 'greetings-new-year': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_07_HAPPY_NEW_YEAR_15.ogg', 'greetings-pirate': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_07_PIRATE_DAY_33.ogg', 'need-weapon': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_07_ERROR01_20.ogg', 'hand-full': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_07_ERROR06_25.ogg', 'picked': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_07_Picked_08.ogg', 'too-many-minions': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_07_ERROR07_26.ogg', 'oops': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_07_Oops_03.ogg', 'start': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_07_Start_09.ogg', 'concede': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_07_Concede_07.ogg', 'greetings-noblegarden': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_07_HAPPY_NOBLEGARDEN_17.ogre-magi'}
uther = {'hero-death': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_04_Death_17.ogg', 'well-played': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_04_WellPlayed_02.ogg', 'hero-attack': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_04_Attack_16.ogg', 'wow': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_04_WOW_06.ogg', 'generic-error': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_04_ERROR12_31.ogg', 'minion-sleep': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_04_ERROR05_24.ogg', 'thinking-3': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_04_Thinking3_14.ogg', 'oops': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_04_Oops_03.ogg', 'greetings-holidays': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_04_HAPPY_HOLIDAYS_14.ogg', 'thanks': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_04_Thanks_05.ogg', 'start': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_04_Start_09.ogg', 'picked': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_04_Picked_08.ogg', 'greetings-pirate': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_04_PIRATE_DAY_33.ogg', 'taunt': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_04_ERROR11_20.ogg', 'hero-attacked': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_04_ERROR04_23.ogg', 'greetings-halloween': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_04_HAPPY_HALLOWEEN_13.ogg', 'limited-time': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_04_Time_11.ogg', 'sorry': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_04_Sorry_06.ogg', 'greetings-new-year': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_04_HAPPY_NEW_YEAR_15.ogg', 'cant-play': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_04_ERROR09_28.ogg', 'thinking-2': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_04_Thinking2_13.ogg', 'invalid-target': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_04_ERROR10_29.ogg', 'mirror': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_04_MIRROR_START_01.ogg', 'minion-attacked': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_04_ERROR03_22.ogg', 'thinking-1': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_04_Thinking1_12.ogg', 'greetings-fire': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_04_FIRE_FESTIVAL_32.ogg', 'stealth': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_04_ERROR08_27.ogg', 'no-cards': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_04_NoCards_19.ogg', 'no-mana': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_04_ERROR02_21.ogg', 'low-cards': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_04_LowCards_18.ogg', 'too-many-minions': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_04_ERROR07_26.ogg', 'weapon-ready': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_04_Weapon_10.ogg', 'greetings': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_04_Greetings_01.ogg', 'concede': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_04_Concede_07.ogg', 'need-weapon': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_04_ERROR01_20.ogg', 'hand-full': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_04_ERROR06_25.ogg', 'threaten':  'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_04_Threaten_04.ogg', 'greetings-noblegarden': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_04_HAPPY_NOBLEGARDEN_17.ogg'}
rexxar = {'hero-death': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_05_Death_17.ogg', 'well-played': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_05_Well Played_02.ogg', 'hero-attack': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_05_Attack_16.ogg', 'greetings-fire': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_05_FIRE_FESTIVAL_32.ogg', 'start': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_05_Start_09.ogg', 'greetings-halloween': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_05_HAPPY_HALLOWEEN_13.ogg', 'limited-time': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_05_Time_11.ogg', 'concede': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_05_Concede_07.ogg', 'greetings-pirate': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_05_PIRATE_DAY_33.ogg', 'no-cards': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_05_NoCards_20.ogg', 'stealth': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_05_ERROR08_28.ogg', 'thinking-1': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_05_Thinking1_12.ogg', 'invalid-target': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_05_ERROR10_30.ogg', 'thinking-2': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_05_Thinking2_13.ogg', 'cant-play': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_05_ERROR09_29.ogg', 'minion-attacked': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_05_ERROR03_23.ogg', 'wow': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_05_WOW_06.ogg', 'weapon-ready': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_05_Weapon_10.ogg', 'greetings-new-year': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_05_HAPPY_NEW_YEAR_15.ogg', 'too-many-minions': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_05_ERROR07_27.ogg', 'need-weapon': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_05_ERROR01_21.ogg', 'no-mana': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_05_ERROR02_22.ogg', 'greetings': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_05_Greetings_01.ogg', 'generic-error': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_05_ERROR12_32.ogg', 'sorry': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_05_Sorry_06.ogg', 'threaten': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_05_Threaten_04.ogg', 'hand-full': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_05_ERROR06_26.ogg', 'oops': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_05_Oops_03.ogg', 'hero-attacked': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_05_ERROR04_24.ogg', 'greetings-holidays': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_05_HAPPY_HOLIDAYS_14.ogg', 'picked': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_05_Picked_08.ogg', 'low-cards': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_05_LowCards_19.ogg', 'thanks': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_05_Thanks_05.ogg', 'minion-sleep': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_05_ERROR05_25.ogg', 'taunt': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_05_ERROR11_20.ogg', 'thinking-3': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_05_Thinking3_14.ogg', 'mirror': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_05_MIRROR_START_01.ogg', 'greetings-noblegarden': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_05_HAPPY_NOBLEGARDEN_17.ogg'}
thrall = {'mirror': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_02_MIRROR_START_ALT_03.ogg', 'greetings-halloween': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_02_HAPPY_HALLOWEEN_05.ogg', 'greetings-holidays': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_02_HAPPY_HOLIDAYS_06.ogg', 'greetings-pirate': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_02_PIRATE_DAY_34.ogg', 'greetings-fire': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_02_FIRE_FESTIVAL_33.ogg', 'wow': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_02_WOW_12_ALT.ogg', 'greetings-new-year': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_02_HAPPY_NEW_YEAR_07.ogg', 'taunt': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_02_ERROR11_21.ogg', 'greetings': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_02_HAPPY_NEW_YEAR_LUNAR_16.ogg', 'greetings-noblegarden': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_02_HAPPY_NOBLEGARDEN_18.ogg'}
valeera = {'hero-death': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_03_Death_17.ogg', 'well-played': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_03_Well Played_02.ogg', 'hero-attack': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_03_Attack_16.ogg', 'start': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_03_Start_09.ogg', 'low-cards': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_03_LowCards_18.ogg', 'minion-attacked': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_03_ERROR03_22.ogg', 'greetings-new-year': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_03_HAPPY_NEW_YEAR_06.ogg', 'hero-attacked': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_03_ERROR04_23.ogg', 'concede': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_03_Concede_07.ogg', 'invalid-target': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_03_ERROR10_29.ogg', 'cant-play': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_03_ERROR09_28.ogg', 'greetings-fire': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_03_FIRE_FESTIVAL_32.ogg', 'taunt': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_03_ERROR11_20.ogg', 'picked': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_03_Picked_08.ogg', 'thanks': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_03_Thanks_05.ogg', 'greetings-holidays': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_03_HAPPY_HOLIDAYS_05.ogg', 'mirror': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_03_MIRROR_START_02.ogg', 'minion-sleep': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_03_ERROR05_24.ogg', 'limited-time': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_03_Time_11.ogg', 'greetings-pirate': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_03_PIRATE_DAY_33.ogg', 'greetings-halloween': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_03_HAPPY_HALLOWEEN_04.ogg', 'hand-full': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_03_ERROR06_25.ogg', 'generic-error': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_03_ERROR12_31.ogg', 'threaten': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_03_Threaten_04.ogg', 'thinking-3': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_03_Thinking3_14.ogg', 'need-weapon': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_03_ERROR01_20.ogg', 'thinking-2': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_03_Thinking2_13.ogg', 'greetings': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_03_Greetings_01.ogg', 'oops': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_03_Oops_03.ogg', 'no-mana': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_03_ERROR02_21.ogg', 'too-many-minions': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_03_ERROR07_26.ogg', 'wow': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_03_WOW_11.ogg', 'stealth': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_03_ERROR08_27.ogg', 'no-cards': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_03_NoCards_19.ogg', 'thinking-1': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_03_Thinking1_12.ogg', 'weapon-ready': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_03_Weapon_10.ogg', 'sorry': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_03_Sorry_06.ogg', 'greetings-noblegarden': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_03_HAPPY_NOBLEGARDEN_17.ogg'}
malfurion = {'hero-death': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_06_Death_17.ogg', 'well-played': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_06_Well Played_02.ogg', 'hero-attack': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_06_Attack_16.ogg', 'low-cards': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_06_LowCards_18.ogg', 'minion-sleep': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_06_ERROR05_24.ogg', 'taunt': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_06_ERROR11_20.ogg', 'mirror': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_06_MIRROR_START_01.ogg', 'weapon-ready': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_06_Weapon_10.ogg', 'need-weapon': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_06_ERROR01_20.ogg', 'greetings-pirate': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_06_PIRATE_DAY_33.ogg', 'greetings-halloween': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_06_HAPPY_HALLOWEEN_13.ogg', 'start': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_06_Threaten_04.ogg', 'start': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_06_Start_09.ogg', 'hand-full': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_06_ERROR06_25.ogg', 'generic-error': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_06_ERROR12_31.ogg', 'stealth': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_06_ERROR08_27.ogg', 'greetings-fire': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_06_FIRE_FESTIVAL_32.ogg', 'greetings-holidays': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_06_HAPPY_HOLIDAYS_14.ogg', 'no-cards': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_06_NoCards_19.ogg', 'limited-time': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_06_Time_11.ogg', 'thinking-2': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_06_Thinking2_13.ogg', 'no-mana': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_06_ERROR02_21.ogg', 'thinking-3': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_06_Thinking3_14.ogg', 'sorry': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_06_Sorry_06.ogg', 'too-many-minions': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_06_ERROR07_26.ogg', 'concede': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_06_Concede_07.ogg', 'greetings': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_06_Greetings_01.ogg', 'hero-attacked': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_06_ERROR04_23.ogg', 'picked': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_06_Picked_08.ogg', 'cant-play': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_06_ERROR09_28.ogg', 'oops': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_06_Oops_03.ogg', 'invalid-target': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_06_ERROR10_29.ogg', 'thanks': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_06_Thanks_05.ogg', 'wow': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_06_WOW_06.ogg', 'thinking-1': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_06_Thinking1_12.ogg', 'start-2': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_06_TYRANDE_36.ogg', 'minion-attacked': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_06_ERROR03_22.ogg', 'greetings-new-year': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_06_HAPPY_NEW_YEAR_15.ogg', 'greetings-noblegarden': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_06_HAPPY_NOBLEGARDEN_17.ogg'}
jaina = {'hero-death': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_08_Death_72.ogg', 'well-played': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_08_Well Played_57.ogg', 'hero-attack': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_08_Attack_71.ogg', 'minion-sleep': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_08_ERROR05_79.ogg', 'taunt': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_08_ERROR11_20.ogg', 'thinking-1': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_08_Thinking1_67.ogg', 'picked': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_08_Picked_63.ogg', 'thanks': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_08_Thanks_60.ogg', 'hero-attacked': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_08_ERROR04_78.ogg', 'greetings-halloween': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_08_HAPPY_HALLOWEEN_13.ogg', 'thinking-2': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_08_Thinking2_68.ogg', 'invalid-target': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_08_ERROR10_84.ogg', 'greetings': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_08_Greetings_56.ogg', 'cant-play': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_08_ERROR09_83.ogg', 'weapon-ready': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_08_Weapon_65.ogg', 'start': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_08_Start_64.ogg', 'minion-attacked': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_08_ERROR03_77.ogg', 'low-cards': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_08_LowCards_73.ogg', 'no-cards': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_08_NoCards_74.ogg', 'greetings-new-year': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_08_HAPPY_NEW_YEAR_15.ogg', 'stealth': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_08_ERROR08_82.ogg', 'concede': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_08_Concede_62.ogg', 'threaten': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_08_Threaten_59.ogg', 'no-mana': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_08_ERROR02_76.ogg', 'sorry': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_08_Sorry_61.ogg', 'too-many-minions': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_08_ERROR07_81.ogg', 'greetings-fire': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_08_FIRE_FESTIVAL_32.ogg', 'mirror': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_08_MIRROR_START_01.ogg', 'limited-time': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_08_Time_66.ogg', 'wow': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_08_WOW_06.ogg', 'need-weapon': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_08_ERROR01_75.ogg', 'greetings-pirate': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_08_PIRATE_DAY_33.ogg', 'hand-full': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_08_ERROR06_80.ogg', 'greetings-holidays': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_08_HAPPY_HOLIDAYS_14.ogg', 'generic-error': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_08_ERROR12_86.ogg', 'thinking-3': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_08_Thinking3_69.ogg', 'oops': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_08_Oops_58.ogg', 'greetings-noblegarden': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_08_HAPPY_NOBLEGARDEN_17.ogg'}
rangaros_hero = {'hero-death': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_BRM_027h_Death_63.ogg', 'well-played': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_BRM_027h_Well_Played_06.ogg', 'hero-attack': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_BRM_027h_Attack_15.ogg', 'greetings-new-year': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_BRM_027h_HAPPY_NEW_YEAR_38.ogg', 'oops': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_BRM_027h_Oops_07.ogg', 'stealth': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_BRM_027h_ERROR08_58.ogg', 'party': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_BRM_027h_PARTY_22.ogg', 'concede': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_BRM_027h_Concede_11.ogg', 'no-mana': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_BRM_027h_ERROR02_52.ogg', 'greetings-pirate': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_BRM_027h_PIRATE_DAY_45.ogg', 'hero-attacked': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_BRM_027h_ERROR04_54.ogg', 'limited-time': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_BRM_027h_Time_48.ogg', 'greetings-event': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_BRM_027h_HAPPY_EVENT_41.ogg', 'no-cards': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_BRM_027h_NoCards_50.ogg', 'invalid-target': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_BRM_027h_ERROR10_60.ogg', 'cant-play': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_BRM_027h_ERROR09_59.ogg', 'thinking-3': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_BRM_027h_Thinking3_14.ogg', 'minion-attacked': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_BRM_027h_ERROR03_53.ogg', 'thinking-2': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_BRM_027h_Thinking2_13.ogg', 'generic-error': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_BRM_027h_ERROR12_62.ogg', 'greetings-fire': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_BRM_027h_FIRE_FESTIVAL_44.ogg', 'celebrate': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_BRM_027h_CELEBRATE_24.ogg', 'low-cards': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_BRM_027h_LowCards_49.ogg', 'greetings-halloween': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_BRM_027h_HAPPY_HALLOWEEN_36.ogg', 'sorry': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_BRM_027h_Sorry_10.ogg', 'minion-sleep': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_BRM_027h_ERROR05_55.ogg', 'taunt': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_BRM_027h_ERROR11_61.ogg', 'too-many-minions': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_BRM_027h_ERROR07_57.ogg', 'greetings-holidays': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_BRM_027h_HAPPY_HOLIDAYS_37.ogg', 'thinking-1': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_BRM_027h_Thinking1_12.ogg', 'threaten': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_BRM_027h_Threaten_08.ogg', 'wow': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_BRM_027h_WOW_20.ogg', 'need-weapon': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_BRM_027h_ERROR01_51.ogg', 'hand-full': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_BRM_027h_ERROR06_56.ogg', 'greetings': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_BRM_027h_Greetings_04.ogg', 'thanks': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_BRM_027h_Thanks_09.ogg', 'greetings-noblegarden': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_BRM_027h_HAPPY_NOBLEGARDEN_39.ogg'}
jaraxxus_hero = { 'well-played': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_EX1_323h_Well Played_06.ogg', 'low-cards': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_EX1_323h_LowCards_19.ogg', 'hero-attack': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_EX1_323_Attack_02.ogg', 'hero-attacked': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_EX1_323h_ERROR04_24.ogg', 'greetings': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_EX1_323h_HAPPY_NEW_YEAR_LUNAR_14.ogg', 'minion-attacked': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_EX1_323h_ERROR03_23.ogg', 'greetings-holidays': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_EX1_323h_HAPPY_HOLIDAYS_12.ogg', 'invalid-target': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_EX1_323h_ERROR10_30.ogg', 'cant-play': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_EX1_323h_ERROR09_29.ogg', 'minion-sleep': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_EX1_323h_ERROR05_25.ogg', 'concede': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_EX1_323h_ConcedeALT_12.ogg', 'sorry': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_EX1_323h_Sorry_10.ogg', 'thanks': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_EX1_323h_Thanks_09.ogg', 'generic-error': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_EX1_323h_ERROR12_32.ogg', 'limited-time': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_EX1_323h_Time_14.ogg', 'greetings-halloween': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_EX1_323h_HAPPY_HALLOWEEN_11.ogg', 'taunt': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_EX1_323h_ERROR11_31.ogg', 'thinking-3': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_EX1_323h_Thinking3_17.ogg', 'greetings-fire': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_EX1_323h_FIRE_FESTIVAL_29.ogg', 'threaten': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_EX1_323h_Threaten_08.ogg', 'greetings-new-year': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_EX1_323h_HAPPY_NEW_YEAR_13.ogg', 'need-weapon': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_EX1_323h_ERROR01_21.ogg', 'wow': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_EX1_323h_WOW_04.ogg', 'thinking-2': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_EX1_323h_Thinking2_16.ogg', 'greetings-pirate': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_EX1_323h_PIRATE_DAY_30.ogg', 'oops': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_EX1_323h_Oops_07.ogg', 'hand-full': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_EX1_323h_ERROR06_26.ogg', 'no-cards': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_EX1_323h_NoCards_20.ogg', 'thinking-1': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_EX1_323h_Thinking1_15.ogg', 'stealth': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_EX1_323h_ERROR08_28.ogg', 'concede-2': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_EX1_323h_Concede_11.ogg', 'weapon-ready': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_EX1_323h_Weapon_13.ogg', 'too-many-minions': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_EX1_323h_ERROR07_27.ogg', 'no-mana': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_EX1_323h_ERROR02_22.ogg', 'greetings-noblegarden': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_EX1_323h_HAPPY_NOBLEGARDEN_15.ogg'}
maiev = {'hero-death': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_03a_DEATH_63.ogg', 'cant-play': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_03a_ERROR_PLAY_27.ogg', 'minion-sleep': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_03a_ERROR_JUST_PLAYED_23.ogg', 'well-played': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_03a_WELL_PLAYED_07.ogg', 'hero-attacked': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_03a_ERROR_I_ATTACKED_22.ogg', 'minion-attacked': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_03a_ERROR_MINION_ATTACKED_21.ogg', 'hero-attack': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_03a_Attack_15.ogg', 'thinking-1': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_03a_THINK1_12.ogg', 'thanks': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_03a_THANKS_09.ogg', 'low-cards': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_03a_LOW_CARDS_17.ogg', 'greetings-new-year': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_03a_HAPPY_NEW_YEAR_53.ogg', 'too-many-minions': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_03a_ERROR_FULL_MINIONS_25.ogg', 'taunt': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_03a_ERROR_TAUNT_29.ogg', 'mirror': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_03a_MIRROR_START_02.ogg', 'threaten': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_03a_THREATEN_05.ogg', 'greetings-fire': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_03a_FIRE_FESTIVAL_59.ogg', 'greetings-pirate': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_03a_PIRATE_DAY_60.ogg', 'concede': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_03a_CONCEDE_06.ogg', 'generic-error': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_03a_ERROR_GENERIC_30.ogg', 'greetings-halloween': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_03a_HAPPY_HALLOWEEN_51.ogg', 'wow': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_03a_WOW_35.ogg', 'start': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_03a_START_01.ogg', 'greetings-holidays': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_03a_HAPPY_HOLIDAYS_52.ogg', 'no-mana': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_03a_ERROR_NEED_MANA_20.ogg', 'no-cards': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_03a_NO_CARDS_18.ogg', 'limited-time': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_03a_TIMER_16.ogg', 'hand-full': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_03a_ERROR_HAND_FULL_24.ogg', 'need-weapon': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_03a_ERROR_NEED_WEAPON_19.ogg', 'invalid-target': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_03a_ERROR_TARGET_28.ogg', 'oops': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_03a_OOPS_08.ogg', 'greetings': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_03a_GREETINGS_03.ogg', 'thinking-2': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_03a_THINK2_13.ogg', 'thinking-3': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_03a_THINK3_14.ogg', 'stealth': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_03a_ERROR_STEALTH_26.ogg', 'sorry': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_03a_SORRY_10.ogg', 'picked': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_03a_PICKED_11.ogg', 'greetings-noblegarden': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_03a_HAPPY_NOBLEGARDEN_54.ogg'}
tyrande = {'hero-death': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_09a_DEATH_63.ogg', 'minion-sleep': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_09a_ERROR_JUST_PLAYED_23.ogg', 'well-played': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_09a_WELL_PLAYED_07.ogg', 'cant-play': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_09a_ERROR_PLAY_27.ogg', 'minion-attacked': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_09a_ERROR_MINION_ATTACKED_21.ogg', 'hero-attacked': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_09a_ERROR_I_ATTACKED_22.ogg', 'hero-attack': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_09a_Attack_15.ogg', 'oops': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_09a_OOPS_08.ogg', 'greetings-holidays': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_09a_HAPPY_HOLIDAYS_52.ogg', 'hand-full': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_09a_ERROR_HAND_FULL_24.ogg', 'wow': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_09a_WOW_35.ogg', 'picked': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_09a_PICKED_11.ogg', 'mirror': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_09a_MIRROR_START_02.ogg', 'no-cards': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_09a_NO_CARDS_18.ogg', 'greetings-halloween': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_09a_HAPPY_HALLOWEEN_51.ogg', 'sorry': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_09a_SORRY_10.ogg', 'thanks': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_09a_THANKS_09.ogg', 'greetings-pirate': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_09a_PIRATE_DAY_60.ogg', 'thinking-1': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_09a_THINK1_12.ogg', 'need-weapon': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_09a_ERROR_NEED_WEAPON_19.ogg', 'concede': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_09a_CONCEDE_06.ogg', 'low-cards': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_09a_LOW_CARDS_17.ogg', 'greetings': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_09a_GREETINGS_03.ogg', 'invalid-target': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_09a_ERROR_TARGET_28.ogg', 'threaten': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_09a_THREATEN_05.ogg', 'greetings-new-year': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_09a_HAPPY_NEW_YEAR_01.ogg', 'stealth': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_09a_ERROR_STEALTH_26.ogg', 'start': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_09a_START_01.ogg', 'taunt': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_09a_ERROR_TAUNT_29.ogg', 'thinking-2': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_09a_THINK2_13.ogg', 'greetings-mirror': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_09a_MIRROR_GREETINGS_04.ogg', 'no-mana': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_09a_ERROR_NEED_MANA_20.ogg', 'thinking-3': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_09a_THINK3_14.ogg', 'too-many-minions': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_09a_ERROR_FULL_MINIONS_25.ogg', 'start-2': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_09a_MALFURION_64.ogg', 'generic-error': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_09a_ERROR_GENERIC_30.ogg', 'greetings-fire': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_09a_FIRE_FESTIVAL_59.ogg', 'limited-time': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_09a_TIMER_16.ogg', 'greetings-noblegarden': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_09a_HAPPY_NOBLEGARDEN_54.ogg'}
khadgar = {'hero-death': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_08b_DEATH_63_ALT.ogg', 'cant-play': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_08b_ERROR_PLAY_27.ogg', 'well-played': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_08b_WELL_PLAYED_07.ogg', 'minion-sleep': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_08b_ERROR_JUST_PLAYED_23.ogg', 'minion-attacked': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_08b_ERROR_MINION_ATTACKED_21.ogg', 'hero-attacked': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_08b_ERROR_I_ATTACKED_22.ogg', 'hero-attack': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_08b_Attack_15.ogg', 'greetings-halloween': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_08b_HAPPY_HALLOWEEN_51.ogg', 'start': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_08b_START_01.ogg', 'generic-error': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_08b_ERROR_GENERIC_30.ogg', 'greetings-new-year': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_08b_HAPPY_NEW_YEAR_53.ogg', 'greetings-fire': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_08b_FIRE_FESTIVAL_59.ogg', 'concede': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_08b_CONCEDE_06.ogg', 'thanks': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_08b_THANKS_09.ogg', 'picked': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_08b_PICKED_11.ogg', 'invalid-target': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_08b_ERROR_TARGET_28.ogg', 'mirror': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_08b_MIRROR_START_02.ogg', 'too-many-minions': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_08b_ERROR_FULL_MINIONS_25.ogg', 'threaten': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_08b_THREATEN_05.ogg', 'taunt': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_08b_ERROR_TAUNT_29.ogg', 'thinking-3': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_08b_THINK3_14.ogg', 'limited-time': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_08b_TIMER_16.ogg', 'greetings-pirate': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_08b_PIRATE_DAY_60.ogg', 'no-mana': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_08b_ERROR_NEED_MANA_20.ogg', 'oops': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_08b_OOPS_08.ogg', 'stealth': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_08b_ERROR_STEALTH_26.ogg', 'sorry': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_08b_SORRY_10.ogg', 'thinking-2': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_08b_THINK2_13.ogg', 'wow': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_08b_WOW_35.ogg', 'thinking-1': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_08b_THINK1_12.ogg', 'low-cards': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_08b_LOW_CARDS_17.ogg', 'need-weapon': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_08b_ERROR_NEED_WEAPON_19.ogg', 'hand-full': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_08b_ERROR_HAND_FULL_24.ogg', 'greetings': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_08b_GREETINGS_03.ogg', 'greetings-mirror': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_08b_MIRROR_GREETINGS_04.ogg', 'greetings-holidays': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_08b_HAPPY_HOLIDAYS_52.ogg', 'no-cards': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_08b_NO_CARDS_18.ogg', 'greetings-noblegarden': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_08b_HAPPY_NOBLEGARDEN_54.ogg'}
hagatha = {'hero-death': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_GIL_504_Female_Orc_Death_01.ogg', 'well-played': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_GIL_504_Female_Orc_Well_Played_01.ogg', 'start': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_GIL_504_Female_Orc_Play_02.ogg', 'hero-attack': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_GIL_504_Female_Orc_Attack_01.ogg', 'thinking-1': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_GIL_504_Female_Orc_Thinking_01.ogg', 'greetings': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_GIL_504_Female_Orc_Greetings_02.ogg', 'thinking-3': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_GIL_504_Female_Orc_Thinking_03.ogg', 'thinking-2': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_GIL_504_Female_Orc_Thinking_02.ogg', 'concede': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_GIL_504_Female_Orc_Concede_01.ogg', 'no-cards': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_GIL_504_Female_Orc_NoCards_01.ogg', 'wow': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_GIL_504_Female_Orc_Wow_01.ogg', 'oops': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_GIL_504_Female_Orc_Oops_01.ogg', 'limited-time': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_GIL_504_Female_Orc_Time_01.ogg', 'threaten': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_GIL_504_Female_Orc_Threaten_02.ogg', 'low-cards': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_GIL_504_Female_Orc_LowCards_01.ogg', 'thanks': 'http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_GIL_504_Female_Orc_Thanks_01.ogg'}
list_of_heroes = [anduin, garrosh, guldan, uther, rexxar, thrall, valeera, malfurion, jaina, rangaros_hero, jaraxxus_hero, maiev, tyrande, khadgar, hagatha]
list_of_hero_names = ['anduin', 'garrosh', 'guldan', 'uther', 'rexxar', 'thrall', 'valeera', 'malfurion', 'jaina', 'rangaros_hero', 'jaraxxus_hero', 'maiev', 'tyrande', 'khadgar', 'hagatha']
#This is a dictionary of any cards that have either a dash, comma, or apostrophe.  I then wrote their forms for the response since the normal cards wont have these written down.
dic_of_grammar = {'cthun': 'C\'thun', 'nzoth-the-corruptor': 'N\'zoth, the Corruptor', 'yogg-saron-hopes-end': 'Yogg-Saron, Hope\'s End','yshaarj-rage-unbound': 'Y\'Shaarj, Rage Unbound',
'anubarak': 'Anub\'arak', 'blade-of-cthun': 'Blade of C\'thun', 'malganis': 'Mal\'ganis', 'alakir-the-windlord': 'Al\'Akir the Windlord', 'kelthuzad': 'Kel\'Thuzad',
'sneeds-old-shredder': 'Sneed\'s Old Shredder', 'arch-thief-rafaam': 'Arch-Thief Rafaam', 'force-tank-max': 'Force-Tank MAX', 'deathwing-dragonlord': 'Deathwing, Dragonlord',
'kalimos-primal-lord': 'Kalimos, Primal Lord', 'medivh-the-guardian': 'Medivh, the Guardian', 'ragnaros-lightlord': "Ragnaros, Lightlord", 'chogall': 'Cho\'Gall', 'don-hancho': 'Don Han\'Cho',
'gahzrilla': 'Gahz\'rilla', 'skycapn-kragg': 'Skycap\'n Kragg', 'twin-emperor-veklor': 'Twin Emperor Vek\'lor', 'hogger-doom-of-elwynn': 'Hogger, Doom of Elwynn',
'grumble-worldshaker': 'Grumble, Worldshaker', 'hemet-jungle-hunter': 'Hemet, Jungle Hunter', 'big-time-racketeer': 'Big-Time Racketeer', 'mogors-champion': 'Mogor\'s Champion',
'blood-queen-lanathel': 'Blood-Queen Lana\'thel', 'mukla-tyrant-of-the-vale': 'Mukla, Tyrant of the Vale', 'rin-the-first-disciple': 'Rin, the First Disciple', 'toki-time-tinker': 'Toki, Time-Tinker',
'bolvar-fireblood': 'Bolvar, Fireblood', 'mech-bear-cat': 'Mech-Bear-Cat', 'wind-up-burglebot': 'Wind-up Burglebot', 'mimirons-head': 'Mimiron\'s Head', 'muklas-champion': 'Mukla\'s Champion',
'finja-the-flying-star': 'Finja, the Flying Star', 'ixlid-fungal-lord': 'Ixlid, Fungal Lord', 'nexus-champion-saraad': 'Nexus-Champion Saraad', 'psych-o-tron': 'Psych-O-Tron',
'second-rate-bruiser': 'Second-Rate Bruiser', 'servant-of-yogg-saron': 'Servant of Yogg-Saron', 'shado-pan-rider':'Shado-Pan Rider', 'sunborne-valkyr': 'Sunborne Val\'kyr',
'tolvir-warden': 'Tol\'vir warden', 'voljin': 'Vol\'jin', 'anubar-ambusher': "Anub\'ar Ambusher", 'cthuns-chosen': 'C\'Thun\'s Chosen', 'faldorei-strider': 'Fal\'dorei Strider',
'arcane-nullifier-x-21': 'Arcane Nullifier X-21', 'bright-eyed-scout': 'Bright-Eyed Scout', 'enhance-o-mechano': 'Enhance-o Mechano', 'genzo-the-shark': 'Genzo, the Shark',
'korkron-elite': 'Kor\'kron Elite', 'mogushan-warden': 'Mogu\'shan Warden', 'senjin-shieldmasta': 'Sen\'jin Shieldmasta', 'sherazin-corpse-flower': 'Sherazin, Corpse Flower',
'gorillabot-a-3': 'Gorillabot A-3', 'klaxxi-amber-weaver': 'Klaxxi Amber-Weaver', 'mini-mage': 'Mini-Mage', 'old-murk-eye': 'Old Murk-Eye', 'tolvir-stoneshaper': 'Tol\'vir Stoneshaper',
'amgam-rager': 'Am\'gam Rager', 'disciple-of-cthun': 'Disciple of C\'thun', 'xaril-poisoned-mind': 'Xaril, Poisoned Mind', 'alarm-o-bot': 'Alarm-O-Bot', 'lights-champion': 'Light\'s Champion',
'lil-exorcist': 'Lil\' Exorcist', 'spawn-of-nzoth': 'Spawn of N\'zoth', 'hench-clan-thug': 'Hench-Clan Thug', 'shaku-the-collector': 'Shaku, the Collector', 'valkyr-soulclaimer': 'Val\'kyr Voulclaimer',
'witchs-cauldron': 'Witch\'s Cauldron', 'alexstraszas-champion': 'Alexstrasza\'s Champion', 'captains-parrot': 'Captain\'s Parrot', 'annoy-o-tron': 'Annoy-o-Tron',
'nat-the-darkfisher': 'Nat, the Darkfisher', 'kings-elekk': 'King\'s Elekk', 'medivhs-valet': 'Medivh\'s Valet', 'nerubar-weblord': 'Nerub\'ar Weblord', 'sorcerers-apprentice': 'Sorcerer\'s Apprentice',
'ships-cannon': 'Ship\'s Cannon', 'goblin-auto-barber': 'Goblin Auto-Barber', 'one-eyed-cheat': 'One-Eyed Cheat', 'pint-sized-summoner': 'Pint-Sized Summoner', 'scorp-o-matic': 'Scorp-o-matic',
'whirling-zap-o-matic': 'Whirling Zap-o-matic', 'small-time-buccaneer': 'Small-Time Buccaneer', 'malchezaars-imp': 'Malchezaar\'s Imp', 'nzoths-first-mate': 'N\'zoth\'s First Mate',
'tentacle-of-nzoth': 'Tentacle of N\'zoth', 'witchs-apprentice': 'Witch\'s Appretice','bloodreaver-guldan': 'Bloodreaver Gul\'dan', 'v-07-tr-on': 'V-07-TR-oN',
'twin-emperor-veknilash': 'Twin Emperor Vek\'nilash', 'little-friend': '"Little Friend"', 'kilrek': 'Kil\'rek', 'carnassas-brood': 'Carnassa\'s Brood', 'azari-the-devourer': 'Azari, the Devourer',
'archmages-apprentice': 'Archmage\'s Apprentice', 'amara-warden-of-hope': 'Amara, Warden of Hope'}

#This is a list of all the minions currently in Hearthstone at the time of Witchwood.  It was made in card_list but copied into center so that the program doesn't have to remake the list each run.

minion_list = ['molten-giant', 'arcane-giant', 'clockwork-giant', 'mountain-giant', 'snowfury-giant', 'cthun', 'deathwing', 'deathwing-dragonlord', 'emeriss', 'faceless-behemoth', 'frost-giant', 'kun-the-forgotten-king', 'nzoth-the-corruptor', 'sea-giant', 'tyrantus', 'ultrasaur', 'varian-wrynn', 'yogg-saron-hopes-end', 'yshaarj-rage-unbound', 'alexstrasza', 'anubarak', 'arch-thief-rafaam', 'aviana', 'baku-the-mooneater', 'blade-of-cthun', 'blood-of-the-ancient-one', 'cenarius', 'dragoncaller-alanna', 'dragonhatcher', 'giant-mastodon', 'hadronox', 'icehowl', 'king-krush', 'king-mosh', 'krul-the-unshackled', 'lord-jaraxxus', 'majordomo-executus', 'malganis', 'malygos', 'master-oakheart', 'mayor-noggenfogger', 'mekgineer-thermaplugg', 'nefarian', 'north-sea-kraken', 'nozdormu', 'obsidian-statue', 'onyxia', 'ozruk', 'shudderwock', 'sleepy-dragon', 'soggoth-the-slitherer', 'voidlord', 'volcanic-lumberer', 'ysera', 'alakir-the-windlord', 'anomalus', 'bonemare', 'cauldron-elemental', 'charged-devilsaur', 'chromaggus', 'deranged-doctor', 'doomcaller', 'eldritch-horror', 'foe-reaper-4000', 'force-tank-max', 'fossilized-devilsaur', 'geosculptor-yip', 'giant-sand-worm', 'gilnean-royal-guard', 'grand-archivist', 'grizzled-guardian', 'grommash-hellscream', 'gruul', 'ironbark-protector', 'kalimos-primal-lord', 'kathrena-winterwisp', 'kelthuzad', 'king-togwaggle', 'marin-the-fox', 'medivh-the-guardian', 'naga-sea-witch', 'primordial-drake', 'ragnaros-the-firelord', 'ragnaros-lightlord', 'rhonin', 'rotface', 'sindragosa', 'sneeds-old-shredder', 'splintergraft', 'splitting-festeroot', 'tess-greymane', 'the-boogeymonster', 'the-lich-king', 'tirion-fordring', 'tortollan-primalist', 'violet-wurm', 'abominable-bowman', 'abyssal-enforcer', 'acidmaw', 'ancient-of-lore', 'ancient-of-war', 'ancient-shieldbearer', 'archbishop-benedictus', 'archmage-antonidas', 'azalina-soulthief', 'baron-geddon', 'blackhowl-gunspire', 'blazecaller', 'bog-creeper', 'bogshaper', 'captured-jormungar', 'chillmaw', 'chogall', 'confessor-paletress', 'core-hound', 'corridor-creeper', 'countess-ashmore', 'darkmire-moonkin', 'don-hancho', 'dr.-boom', 'eadric-the-pure', 'fearsome-doomguard', 'flame-leviathan', 'furious-ettin', 'gahzrilla', 'giant-anaconda', 'grimestreet-protector', 'grotesque-dragonhawk', 'guardian-of-kings', 'hogger-doom-of-elwynn', 'inkmaster-solia', 'jade-chieftain', 'knight-of-the-wild', 'lord-godfrey', 'lynessa-sunsorrow', 'malkorok', 'malorne', 'neptulon', 'nightscale-matriarch', 'obsidian-destroyer', 'prophet-velen', 'ravenholdt-assassin', 'rend-blackhand', 'sated-threshadon', 'silver-vanguard', 'skycapn-kragg', 'spiteful-summoner', 'stone-sentinel', 'stormwatcher', 'stormwind-champion', 'swamp-king-dred', 'tar-lord', 'temporus', 'the-curator', 'troggzor-the-earthinator', 'twin-emperor-veklor', 'volcanosaur', 'war-golem', 'worgen-abomination', 'wyrmguard', 'ancient-harbinger', 'ancient-of-blossoms', 'anima-golem', 'archmage', 'argent-commander', 'aya-blackpaw', 'big-time-racketeer', 'blackguard', 'bolf-ramshield', 'bone-drake', 'book-wyrm', 'boulderfist-ogre', 'cabal-shadow-priest', 'cairne-bloodhoof', 'coffin-crasher', 'coldarra-drake', 'corrupted-seer', 'cruel-dinomancer', 'crystal-lion', 'cursed-castaway', 'dark-arakkoa', 'defias-cleaner', 'drakonid-crusher', 'dread-infernal', 'emperor-thaurissan', 'faceless-summoner', 'fight-promoter', 'fire-elemental', 'frost-elemental', 'frozen-crusher', 'furnacefire-colossus', 'gadgetzan-auctioneer', 'gazlowe', 'gelbin-mekkatorque', 'gemstudded-golem', 'genn-greymane', 'glinda-crowskin', 'grand-crusader', 'grumble-worldshaker', 'hemet-jungle-hunter', 'herald-volazj', 'hogger', 'hungry-ettin', 'illidan-stormrage', 'iron-juggernaut', 'ivory-knight', 'jade-behemoth', 'justicar-trueheart', 'kabal-crystal-runner', 'kabal-trafficker', 'kidnapper', 'kodorider', 'lady-in-white', 'leatherclad-hogleader', 'lord-of-the-arena', 'luckydo-buccaneer', 'madam-goya', 'maexxna', 'master-jouster', 'mech-bear-cat', 'menagerie-warden', 'moat-lurker', 'mogor-the-ogre', 'mogors-champion', 'moorabi', 'mossy-horror', 'mukla-tyrant-of-the-vale', 'mysterious-challenger', 'necrotic-geist', 'nerubian-prophet', 'nerubian-unraveler', 'ornery-direhorn', 'piloted-sky-golem', 'possessed-lackey', 'priestess-of-elune', 'reckless-rocketeer', 'reno-jackson', 'rin-the-first-disciple', 'sabretooth-stalker', 'savannah-highmane', 'scaled-nightmare', 'sea-reaver', 'seeping-oozeling', 'shieldmaiden', 'sideshow-spelleater', 'skeram-cultist', 'skulking-geist', 'spectral-pillager', 'spellweaver', 'sunkeeper-tarim', 'sunwalker', 'sylvanas-windrunner', 'temple-enforcer', 'the-beast', 'the-black-knight', 'the-mistcaller', 'the-skeleton-knight', 'thing-from-below', 'toki-time-tinker', 'toshley', 'trade-prince-gallywix', 'void-crusher', 'volcanic-drake', 'wilfred-fizzlebang', 'windfury-harpy', 'wind-up-burglebot', 'wobbling-runts', 'wrathion', 'abomination', 'alley-armorsmith', 'antique-healbot', 'anubisath-sentinel', 'arcane-tyrant', 'avian-watcher', 'azure-drake', 'bewitched-guardian', 'big-game-hunter', 'bittertide-hydra', 'blackwing-corruptor', 'blingtron-3000', 'blood-queen-lanathel', 'bloodworm', 'bolvar-fordragon', 'bolvar-fireblood', 'bomb-lobber', 'bomb-squad', 'bone-baron', 'bonfire-elemental', 'booty-bay-bodyguard', 'burgly-bully', 'captain-greenskin', 'carnivorous-cube', 'carrion-drake', 'chief-inspector', 'clockwork-automaton', 'clockwork-knight', 'cobalt-guardian', 'cobalt-scalebane',
'corpse-raiser', 'corpse-widow', 'corrosive-sludge', 'corrupted-healbot', 'crazed-worshipper', 'cryomancer', 'cult-apothecary', 'curio-collector', 'darius-crowley', 'dark-iron-skulker', 'darkscale-healer', 'darkshire-alchemist', 'darkspeaker', 'death-revenant', 'deathweb-spider', 'despicable-dreadlord', 'direhorn-hatchling', 'djinni-of-zephyrs', 'dollmaster-dorian', 'doomguard', 'doppelgangster', 'dragon-consort', 'drakonid-operative', 'druid-of-the-claw', 'druid-of-the-fang', 'duskfallen-aviana', 'earth-elemental', 'elise-the-trailblazer', 'elite-tauren-chieftain', 'ethereal-conjurer', 'ethereal-peddler', 'faceless-manipulator', 'fatespinner', 'fel-reaver', 'fen-creeper', 'festeroot-hulk', 'feugen', 'finja-the-flying-star', 'floating-watcher', 'frostwolf-warlord', 'fungalmancer', 'furbolg-mossbinder', 'ghostly-charger', 'glitter-moth', 'gloom-stag', 'green-jelly', 'grim-patron', 'grimestreet-enforcer', 'grook-fu-master', 'guild-recruiter', 'gurubashi-berserker', 'hallazeal-the-ascended', 'harrison-jones', 'hemet-nesingwary', 'ixlid-fungal-lord', 'junkbot', 'kabal-songstealer', 'king-of-beasts', 'knuckles', 'kvaldir-raider', 'leeroy-jenkins', 'loatheb', 'lotus-agents', 'lotus-assassin', 'lyra-the-sunshard', 'madder-bomber', 'menagerie-magician', 'mimirons-head', 'muck-hunter', 'muklas-champion', 'nesting-roc', 'nexus-champion-saraad', 'nightblade', 'ogre-ninja', 'onyx-bishop', 'pit-fighter', 'prince-liam', 'prince-malchezaar', 'princess-huhuran', 'psych-o-tron', 'quartermaster', 'quartz-elemental', 'ram-wrangler', 'raza-the-chained', 'recruiter', 'red-mana-wyrm', 'rotten-applebaum', 'salty-dog', 'second-rate-bruiser', 'servant-of-kalimos', 'servant-of-yogg-saron', 'shado-pan-rider', 'shadowcaster', 'siege-engine', 'silver-hand-knight', 'skelemancer', 'sludge-belcher', 'spectral-knight', 'spiked-hogrider', 'spiteful-smith', 'stalagg', 'stampeding-kodo', 'starving-buzzard', 'stormpike-commando', 'stranglethorn-tiger', 'streetwise-investigator', 'summoning-stone', 'sunborne-valkyr', 'tar-lurker', 'thunder-bluff-valiant', 'tolvir-warden', 'tomb-lurker', 'trogg-gloomeater', 'tundra-rhino', 'tuskarr-jouster', 'twilight-darkmender', 'upgraded-repair-bot', 'usher-of-souls', 'validated-doomsayer', 'venomancer', 'venture-co.-mercenary', 'verdant-longneck', 'vilebrood-skitterer', 'vilespine-slayer', 'virmen-sensei', 'voljin', 'voodoo-hexxer', 'white-eyes', 'windshear-stormcaller', 'witchwood-grizzly', 'aberrant-berserker', 'ancient-brewmaster', 'ancient-mage', 'ancient-shade', 'animated-armor', 'anubar-ambusher', 'arathi-weaponsmith', 'arcane-keysmith', 'arcane-nullifier-x-21', 'arcanosmith', 'arfus', 'armored-warhorse', 'arrogant-crusader', 'astral-tiger', 'auchenai-soulpriest', 'axe-flinger', 'backroom-bouncer', 'barnes', 'baron-rivendare', 'bellringer-sentry', 'blackwater-pirate', 'blood-witch', 'bloodhoof-brave', 'bright-eyed-scout', 'burly-rockjaw-trogg', 'chillblade-champion', 'chillwind-yeti', 'core-rager', 'corpsetaker', 'crowd-favorite', 'crystalweaver', 'cthuns-chosen', 'cult-master', 'cursed-disciple', 'cyclopian-horror', 'dalaran-aspirant', 'daring-reporter', 'dark-iron-dwarf', 'deathaxe-punisher', 'defender-of-argus', 'demented-frostcaller', 'dispatch-kodo', 'draenei-totemcarver', 'dragonkin-sorcerer', 'dragonling-mechanic', 'dread-corsair', 'dreadsteed', 'dunemaul-shaman', 'duskbreaker', 'eater-of-secrets', 'ebon-dragonsmith', 'eerie-statue', 'elise-starseeker', 'elven-minstrel', 'enhance-o-mechano', 'ethereal-arcanist', 'evil-heckler', 'evolved-kobold', 'exploding-bloatbat', 'faceless-shambler', 'faldorei-strider', 'fandral-staghelm', 'fel-cannon', 'felsoul-inquisitor', 'fire-plume-phoenix', 'fireguard-destroyer', 'flamewreathed-faceless', 'forest-guide', 'frigid-snobold', 'gentle-megasaur', 'genzo-the-shark', 'ghastly-conjurer', 'gnomish-inventor', 'goblin-blastmage', 'gorillabot-a-3', 'gormok-the-impaler', 'grave-shambler', 'grim-necromancer', 'grimy-gadgeteer', 'hoarding-dragon', 'holy-champion', 'hooded-acolyte', 'hooked-reaver', 'houndmaster', 'houndmaster-shaw', 'hozen-healer', 'hungry-dragon', 'infested-tauren', 'infested-wolf', 'ironwood-golem', 'jade-spirit', 'jeeves', 'jinyu-waterspeaker', 'jungle-moonkin', 'kabal-chemist', 'kazakus', 'keening-banshee', 'keeper-of-the-grove', 'keeper-of-uldaman', 'kezan-mystic', 'klaxxi-amber-weaver', 'kobold-illusionist', 'kobold-monk', 'kooky-chemist', 'korkron-elite', 'lakkari-felhound', 'leyline-manipulator', 'lifedrinker', 'lightfused-stegodon', 'lightspawn', 'lilian-voss', 'lost-tallstrider', 'lotus-illusionist', 'mad-hatter', 'magnataur-alpha', 'maiden-of-the-lake', 'master-of-disguise', 'master-of-evolution', 'meat-wagon', 'mechanical-yeti', 'midnight-drake', 'militia-commander', 'mini-mage', 'mire-keeper', 'mistwraith', 'mogushan-warden', 'murloc-knight', 'naga-corsair', 'night-howler', 'night-prowler', 'oasis-snapjaw', 'ogre-magi', 'old-murk-eye', 'phantom-freebooter', 'piloted-shredder', 'pit-lord', 'polluted-hoarder', 'priest-of-the-feast', 'prince-valanar', 'professor-putricide', 'rattling-rascal', 'ravenous-pterrordax', 'refreshment-vendor', 'rumbling-elemental', 'runeforge-haunter', 'sandbinder', 'saronite-chain-gang', 'savage-combatant', 'scaleworm', 'screwjank-clunker', 'seadevil-stinger', 'senjin-shieldmasta', 'shadow-sensei', 'shellshifter', 'sherazin-corpse-flower', 'shifting-shade', 'shimmering-courser', 'shroom-brewer', 'siltfin-spiritwalker', 'silvermoon-guardian', 'sneaky-devil', 'southsea-squidface', 'spawn-of-shadows', 'spellbreaker', 'spiritsinger-umbra', 'steam-surger', 'stegodon', 'stormwind-knight', 'strongshell-scavenger', 'summoning-portal', 'swift-messenger', 'tanaris-hogchopper', 'the-darkness', 'the-glass-knight', 'the-voraxx', 'ticking-abomination', 'tolvir-stoneshaper', 'tomb-pillager', 'tomb-spider', 'tortollan-shellraiser', 'totem-cruncher', 'tournament-medic', 'toxmonger', 'twilight-drake', 'twilight-guardian', 'twilight-summoner', 'unpowered-steambot', 'vex-crow', 'violet-teacher', 'voidcaller', 'wailing-soul', 'water-elemental', 'wee-spellstopper', 'wicked-skeleton', 'wicked-witchdoctor', 'wildwalker', 'windspeaker', 'witchwood-piper', 'worgen-greaser', 'xaril-poisoned-mind', 'acolyte-of-agony', 'acolyte-of-pain', 'addled-grizzly', 'alarm-o-bot', 'aldor-peacekeeper', 'amgam-rager', 'arcane-golem', 'argent-horserider', 'auctionmaster-beardo', 'backstreet-leper', 'bearshark', 'benevolent-djinn', 'black-cat', 'blackwald-pixie', 'blackwing-technician', 'blink-fox', 'blood-knight', 'bloodsail-cultist', 'blubber-baron', 'boisterous-bard', 'brann-bronzebeard', 'carrion-grub', 'cave-hydra', 'celestial-dreamer', 'chittering-tunneler', 'cloaked-huntress', 'coldlight-oracle', 'coldlight-seer', 'coldwraith', 'coliseum-manager', 'crypt-lord', 'curious-glimmerroot', 'cutthroat-buccaneer', 'dalaran-mage', 'dancing-swords', 'dark-cultist', 'darkshire-councilman', 'deadly-fork', 'deathlord', 'deathspeaker', 'demolisher', 'desert-camel', 'devilsaur-egg', 'disciple-of-cthun', 'doomed-apprentice', 'dragonhawk-rider', 'dragonslayer', 'drakkari-defender', 'drakkari-enchanter', 'dreadscale', 'druid-of-the-flame', 'druid-of-the-scythe', 'duskbat', 'duskhaven-hunter', 'earthen-ring-farseer', 'edwin-vancleef', 'eggnapper', 'elder-longneck', 'emperor-cobra', 'eydis-darkbane', 'face-collector', 'fel-orc-soulfiend', 'felguard', 'fencing-coach', 'fierce-monkey', 'fjola-lightbane', 'flamewaker', 'flesheating-ghoul', 'flying-machine', 'forlorn-stalker', 'frothing-berserker', 'fungal-enchanter', 'giant-wasp', 'gilded-gargoyle', 'gluttonous-ooze', 'gnomeregan-infantry', 'gnomish-experimenter', 'goblin-sapper', 'greedy-sprite', 'grimestreet-pawnbroker', 'grimestreet-smuggler', 'grove-tender', 'happy-ghoul', 'harvest-golem', 'hench-clan-thug', 'hired-gun', 'hobgoblin', 'hot-spring-guardian', 'howlfiend', 'howling-commander', 'humongous-razorleaf', 'hyldnir-frostrider', 'ice-rager', 'igneous-elemental', 'illuminator', 'imp-gang-boss', 'imp-master', 'injured-blademaster', 'iron-sensei', 'ironbeak-owl', 'ironforge-rifleman', 'ironfur-grizzly', 'jungle-panther', 'kabal-courier', 'kabal-talonpriest', 'king-mukla', 'kirin-tor-mage', 'kobold-apprentice', 'kobold-barbarian', 'lights-champion', 'lil-exorcist', 'lone-champion', 'magma-rager', 'mana-tide-totem', 'manic-soulcaster', 'marsh-drake', 'master-of-ceremonies', 'metaltooth-leaper', 'mind-control-tech', 'mindbreaker', 'mirage-caller', 'moroes', 'mountainfire-armor', 'mounted-raptor', 'murloc-warleader', 'nightbane-templar', 'nightmare-amalgam', 'ogre-brute', 'orgrimmar-aspirant', 'pantry-spider', 'paragon-of-light', 'phantom-militia', 'plague-scientist', 'primalfin-lookout', 'prince-taldaram', 'pterrordax-hatchling', 'pumpkin-peasant', 'questing-adventurer', 'rabid-worgen', 'raging-worgen', 'raid-leader', 'rat-pack', 'ratcatcher', 'ravaging-ghoul', 'ravencaller', 'razorfen-hunter', 'rummaging-kobold', 'saboteur', 'scarlet-crusader', 'scarlet-purifier', 'sergeant-sally', 'sewer-crawler', 'shade-of-naxxramas', 'shadow-rager', 'shadowfiend', 'shady-dealer', 'shaku-the-collector', 'shaky-zipgunner', 'shallow-gravedigger', 'shattered-sun-cleric', 'shrieking-shroom', 'si-7-agent', 'silent-knight', 'silithid-swarmer', 'silver-hand-regent', 'silverback-patriarch', 'silverware-golem', 'sonya-shadowdancer', 'soot-spewer', 'southsea-captain', 'spawn-of-nzoth', 'spellslinger', 'spider-tank', 'squirming-tentacle', 'stablemaster', 'steward-of-darkshire', 'stitched-tracker', 'stonehill-defender', 'stoneskin-basilisk', 'stoneskin-gargoyle', 'street-trickster', 'tanglefur-mystic', 'tar-creeper', 'tauren-warrior', 'terrorscale-stalker', 'thrallmar-farseer', 'thunder-lizard', 'tinkertown-technician', 'tinkmaster-overspark', 'toothy-chest', 'toxic-sewer-ooze', 'tuskarr-totemic', 'twilight-acolyte', 'twilight-elder', 'twilight-flamecaller', 'unbound-elemental', 'unearthed-raptor', 'unlicensed-apothecary', 'valkyr-soulclaimer', 'vicious-fledgling', 'violet-illusionist', 'void-ripper', 'void-terror', 'voodoo-doll', 'vryghoul', 'walnut-sprite', 'warhorse-trainer', 'warsong-commander', 'wickerflame-burnbristle', 'witchs-cauldron', 'wolfrider', 'zola-the-gorgon', 'zoobot', 'acidic-swamp-ooze', 'alexstraszas-champion', 'amani-berserker', 'ancient-watcher', 'annoy-o-tron', 'anodized-robo-cub', 'arcanologist', 'archmage-arugal', 'argent-protector', 'argent-watchman', 'armorsmith', 'baleful-banker', 'beckoner-of-evil', 'bilefin-tidehunter', 'biteweed', 'bloodfen-raptor', 'bloodmage-thalnos', 'bloodsail-raider', 'blowgill-sniper', 'bluegill-warrior', 'boneguard-lieutenant', 'brrrloc', 'captains-parrot', 'cathedral-gargoyle', 'cavern-shinyfinder', 'clutchmother-zavas', 'cornered-sentry', 'crackling-razormaw', 'crazed-alchemist', 'cruel-taskmaster', 'cult-sorcerer', 'cutpurse', 'dark-peddler', 'darkshire-librarian', 'darnassus-aspirant', 'defias-ringleader', 'dire-wolf-alpha', 'dirty-rat', 'doomsayer', 'druid-of-the-saber', 'druid-of-the-swarm', 'drygulch-jailor', 'drywhisker-armorer', 'duskboar', 'echoing-ooze', 'eternal-sentinel', 'explosive-sheep', 'faerie-dragon', 'fallen-hero', 'fallen-sun-cleric', 'fire-plume-harbinger', 'flame-juggler', 'flametongue-totem', 'friendly-bartender', 'frostwolf-grunt', 'gadgetzan-ferryman', 'gadgetzan-socialite', 'garrison-commander', 'ghost-light-angler', 'gilblin-stalker', 'gnomeferatu', 'goblin-auto-barber', 'golakka-crawler', 'grimestreet-informant', 'grimestreet-outfitter', 'haunted-creeper', 'hobart-grapplehammer', 'huge-toad', 'hunting-mastiff', 'hydrologist', 'ice-walker', 'jade-swarmer', 'jeweled-scarab', 'kindly-grandmother', 'kings-elekk', 'knife-juggler', 'kobold-geomancer', 'kobold-hermit', 'lance-carrier', 'lightwell', 'loot-hoarder', 'lorewalker-cho', 'lost-spirit', 'mad-bomber', 'mad-scientist', 'mana-addict', 'mana-geode', 'mana-wraith', 'master-swordsmith', 'mechwarper', 'medivhs-valet', 'micro-machine', 'millhouse-manastorm', 'mistress-of-pain', 'murkspark-eel', 'murloc-tidehunter', 'murmuring-elemental', 'museum-curator', 'nat-pagle', 'nat-the-darkfisher', 'nerubar-weblord', 'nerubian-egg', 'netherspite-historian', 'novice-engineer', 'one-eyed-cheat', 'patient-assassin', 'pint-sized-summoner', 'plated-beetle', 'pompous-thespian', 'primalfin-champion', 'primalfin-totem', 'prince-keleseth', 'public-defender', 'puddlestomper', 'pyros', 'radiant-elemental', 'ravasaur-runt', 'raven-familiar', 'razorpetal-lasher', 'recombobulator', 'redband-wasp', 'river-crocolisk', 'rockpool-hunter', 'scavenging-hyena', 'scorp-o-matic', 'shadow-ascendant', 'shadowboxer', 'shielded-minibot', 'shimmering-tempest', 'ships-cannon', 'shrinkmeister', 'snowchugger', 'sorcerers-apprentice', 'sparring-partner', 'spellshifter', 'squashling', 'steamwheedle-sniper', 'stonesplinter-trogg', 'stubborn-gastropod', 'succubus', 'sunfury-protector', 'tainted-zealot', 'tiny-knight-of-evil', 'tortollan-forager', 'totem-golem', 'trogg-beastrager', 'tuskarr-fisherman', 'twilight-geomancer', 'twisted-worgen', 'undercity-huckster', 'undercity-valiant', 'unstable-ghoul', 'vicious-scalehide', 'vitality-totem', 'volatile-elemental', 'vulgar-homunculus', 'whirling-zap-o-matic', 'wild-pyromancer', 'wrathguard', 'wyrmrest-agent', 'youthful-brewmaster', 'abusive-sergeant', 'acherus-veteran', 'air-elemental', 'alleycat', 'angry-chicken', 'animated-berserker', 'arcane-anomaly', 'arcane-artificer', 'argent-squire', 'babbling-book', 'bladed-cultist', 'blood-imp', 'bloodsail-corsair', 'brave-archer', 'buccaneer', 'chameleos', 'clockwork-gnome', 'cogmaster', 'crystalline-oracle', 'deadscale-knight', 'dire-mole', 'dragon-egg', 'dust-devil', 'elven-archer', 'emerald-hive-queen', 'emerald-reaver', 'enchanted-raven', 'feral-gibberer', 'fiery-bat', 'fire-fly', 'flame-imp', 'forbidden-ancient', 'gadgetzan-jouster', 'glacial-shard', 'goldshire-footman', 'gravelsnout-knight', 'grimscale-chum', 'grimscale-oracle', 'hungry-crab', 'injured-kvaldir', 'jeweled-macaw', 'kabal-lackey', 'kobold-librarian', 'leper-gnome', 'lightwarden', 'lowly-squire', 'malchezaars-imp', 'mana-wyrm', 'meanstreet-marshal', 'mistress-of-mixtures', 'murloc-raider', 'murloc-tidecaller', 'northshire-cleric', 'nzoths-first-mate', 'patches-the-pirate', 'pit-snake', 'possessed-villager', 'raptor-hatchling', 'reliquary-seeker', 'righteous-protector', 'runic-egg', 'sanguine-reveler', 'secretkeeper', 'selfless-hero', 'shadowbomber', 'shieldbearer', 'shifter-zerus', 'sir-finley-mrrgglton', 'small-time-buccaneer', 'southsea-deckhand', 'stonetusk-boar', 'swamp-dragon-egg', 'swamp-leech', 'swashburglar', 'tentacle-of-nzoth', 'timber-wolf', 'tournament-attendee', 'town-crier', 'tunnel-trogg', 'twilight-whelp', 'undertaker', 'vilefin-inquisitor', 'voidwalker', 'voodoo-doctor', 'warbot', 'wax-elemental', 'weasel-tunneler', 'webspinner', 'witchs-apprentice', 'witchwood-imp', 'worgen-infiltrator', 'wretched-tiller', 'young-dragonhawk', 'young-priestess', 'zealous-initiate', 'zombie-chow', 'murloc-tinyfin', 'snowflipper-penguin', 'target-dummy', 'wisp', 'shadowreaper-anduin', 'thrall-deathseer', 'frost-lich-jaina', 'scourgelord-garrosh', 'valeera-the-hollow', 'bloodreaver-guldan', 'uther-of-the-ebon-blade', 'malfurion-the-pestilent',
'wrath-of-air-totem', 'worthless-imp', 'woodchip', 'wisp', 'wily-runt', 'white-rook', 'white-queen', 'white-pawn', 'white-knight', 'white-bishop', 'whelp', 'wax-rager', 'violet-apprentice', 'v-07-tr-on', 'twin-emperor-veknilash', 'twilight-elemental', 'treant', 'the-storm-guardian', 'the-ancient-one', 'thaddius', 'teapot', 'tabby-cat', 'stoneclaw-totem', 'stone-elemental', 'steward', 'squirrel', 'squire', 'spirit-wolf', 'spider', 'spellbender', 'spectral-spider', 'snake', 'slime', 'skeleton', 'skeletal-flayer', 'skeletal-enforcer', 'silver-hand-recruit', 'silver-hand-murloc', 'sheep', 'shadowbeast', 'shadow-of-nothing', 'searing-totem', 'scarab-beetle', 'scarab', 'romulo', 'rock-elemental', 'repair-bot', 'rat', 'rascally-runt', 'raptor-patriarch', 'raptor', 'queen-carnassa', 'pyros', 'pyros-1', 'pyros-2', 'pumpkin-peasant-1', 'pterrordax', 'primalfin', 'poultryizer', 'portable-ice-wall', 'plate', 'plant', 'pitcher', 'piranha', 'pawn', 'party-portal', 'panther', 'pandaren-scout', 'ooze', 'nether-imp', 'nerubian', 'murloc-scout', 'murloc-razorgill', 'murloc', 'mummy-zombie', 'mr.-bigglesworth', 'misha', 'mirror-image', 'megafin', 'mechanical-dragonling', 'mastiff', 'master-chest', 'mana-treant', 'loyal-sidekick', 'little-friend', 'leyline-spider', 'leokk', 'laughing-sister', 'knife', 'kilrek', 'iron-golem', 'infernal', 'imp', 'icky-tentacle', 'icky-imp', 'hyena', 'huffer', 'hound', 'homing-chicken', 'healing-totem', 'grumbly-runt', 'golden-monkey', 'golden-kobold', 'gnoll', 'ghoul-infestor', 'ghoul', 'galvadon', 'frozen-champion', 'frost-widow', 'frog', 'fork', 'flying-monkey', 'flame-of-azzinoth', 'flame-elemental', 'finkle-einhorn', 'emerald-drake', 'emboldener-3000', 'duskhaven-hunter-1', 'druid-of-the-swarm-1', 'druid-of-the-swarm-3', 'druid-of-the-swarm-4', 'druid-of-the-scythe-1', 'druid-of-the-scythe-2', 'druid-of-the-scythe-3', 'druid-of-the-fang-1', 'druid-of-the-claw-1','druid-of-the-claw-2', 'druid-of-the-claw-3', 'druid-of-the-flame-1', 'druid-of-the-flame-2', 'druid-of-the-flame-3', 'dragon-spirit', 'dorothee', 'direhorn-matriarch', 'devilsaur', 'defias-bandit', 'defender', 'damaged-golem', 'cup', 'crystal', 'splitting-sapling', 'chromatic-dragonkin', 'chicken', 'cellar-spider', 'cat-in-a-hat', 'carnassas-brood', 'candle', 'broom', 'boom-bot', 'boar', 'black-rook', 'black-queen', 'black-pawn', 'black-knight', 'black-bishop', 'big-bad-wolf', 'barnabus-the-stomper', 'baine-bloodhoof', 'azari-the-devourer', 'archmages-apprentice', 'animated-shield', 'amara-warden-of-hope', 'abyssal', 'gilnean-royal-guard-1', 'hyena', 'spellshifter-1', 'swift-messanger-1', 'bat', 'cursed-revenant', 'darion-mograine', 'deathlord-nazgrim', 'doom-rat', 'drakeslayer', 'faceless-destroyer', 'fire-drake', 'giant-rat', 'gnoll-1', 'green-ooze', 'grub', 'guardian-spirit', 'guardian-spirit-1', 'guardian-spirit-2', 'inquisitor-whitemane', 'kabal-demon', 'mithril-golem', 'moss-elemental', 'muckling', 'nether-portal', 'nightscale-whelp', 'sapling', 'thoras-trollbane', 'war-kodo', 'weeping-ghost', 'weeping-ghost-1', 'weeping-ghost-2',  'wolf', 'bronze-broodmother', 'cavern-dreamer', 'draconic-herald', 'harbringer-of-catastrophe', 'infinite-murloc', 'infinite-wolf', 'master-of-realities', 'possibility-seeker', 'rift-warden', 'stasis-dragon', 'stasis-elemental', 'temporal-anomaly', 'thief-of-futures', 'timebound-giant', 'timeline-witness', 'timeway-wanderer', 'wee-whelp', 'wildlands-adventurer', 'black-whelp', 'sabertooth-panther', 'sabertooth-lion', 'sabertooth-tiger', 'dopplegangster-1', 'dopplegangster-2', 'chromie', 'murozond']



dic_of_nicknames = {'4-mana-7/7': 'flamewreathed-faceless', 'dr.-7': 'dr.-boom', 'rag': 'ragnaros-the-firelord', 'happy-rag': 'ragnaros-lightlord', 'flappy-bird': 'vicious-fledgling',
'a-turtle': 'malganis', 'turtle': 'malganis', 'yogg': 'yogg-saron-hopes-end', 'frog-saron': 'yogg-saron-hopes-end', 'frog-saron-hopes-end': 'yogg-saron-hopes-end', 'nzoth': 'nzoth-the-corruptor',
'yshaarj': 'yshaarj-rage-unbound'}

cthun_triggers = ['/hs/sounds/enus/VO_OG_280_Male_OldGod_InPlay_02.ogg', '/hs/sounds/enus/VO_OG_280_Male_OldGod_InPlay_03.ogg', '/hs/sounds/enus/VO_OG_280_Male_OldGod_InPlay_01.ogg', '/hs/sounds/enus/VO_OG_280_Male_OldGod_InPlay_06.ogg', '/hs/sounds/enus/VO_OG_280_Male_OldGod_InPlay_07.ogg', '/hs/sounds/enus/VO_OG_280_Male_OldGod_InPlay_04.ogg', '/hs/sounds/enus/VO_OG_280_Male_OldGod_InPlay_05.ogg',  '/hs/sounds/enus/VO_OG_280_Male_OldGod_InPlay_08.ogg', '/hs/sounds/enus/VO_OG_280_Male_OldGod_InPlay_09.ogg', '/hs/sounds/enus/VO_OG_280_Male_OldGod_InPlay_10.ogg', '/hs/sounds/enus/VO_OG_280_Male_OldGod_InPlay_11.ogg', '/hs/sounds/enus/VO_OG_280_Male_OldGod_InPlay_12.ogg', ]
nefarian_plays = {'warlock': '/hs/sounds/enus/VO_BRMA13_1_HP_WARLOCK_10.ogg', 'priest': 'hs/sounds/enus/VO_BRMA13_1_HP_PRIEST_08.ogg', 'warrior': '/hs/sounds/enus/VO_BRMA13_1_HP_WARRIOR_09.ogg', 'druid': '/hs/sounds/enus/VO_BRMA13_1_HP_DRUID_14.ogg', 'mage': '/hs/sounds/enus/VO_BRMA13_1_HP_MAGE_11.ogg', 'rogue': '/hs/sounds/enus/VO_BRMA13_1_HP_ROGUE_15.ogg', 'paladin': '/hs/sounds/enus/VO_BRMA13_1_HP_PALADIN_07.ogg', 'shaman': '/hs/sounds/enus/VO_BRMA13_1_HP_SHAMAN_13.ogg,', 'hunter': '/hs/sounds/enus/VO_BRMA13_1_HP_HUNTER_12.ogg'}

list_of_exceptions = ['C\'thun', 'Y\'Shaarj, Rage Unbound', 'Nefarian', 'N\'zoth, the Corruptor', 'Rend Blackhand', 'Emperor Thaurissan', 'Majordomo Executus']
#The link to almost any minion in hearthhead is always http://www.hearthhead.com/cards/ followed by the minion's name (without any punctuation or capitalization and with all spaces replaced with -)
card_link_start = "http://www.hearthhead.com/cards/"
audio_link_start = 'http://media.services.zam.com/v1/media/byName/'
#The event list is a list of the terms people can use to call the bot and decide the type of line they want.
event_list = ['attack','play','death','trigger']
#These are empty variables that will be used later.
the_card = ''
the_event = ''
the_reply = ''
the_card2 = ''
the_event2 = ''
the_reply2 = ''
the_card3 = ''
the_event3 = ''
the_reply3 = ''
the_card4 = ''
the_event4 = ''
the_reply4 = ''
the_card5 = ''
the_event5 = ''
the_reply5 = ''
the_card6 = ''
the_event6 = ''
the_reply6 = ''
the_card7 = ''
the_event7 = ''
the_reply7 = ''
the_card8 = ''
the_event8 = ''
the_reply8 = ''
the_card9 = ''
the_event9 = ''
the_reply9 = ''
the_card10 = ''
the_event10 = ''
the_reply10 = ''
comment_list = []
cache = []
dice_roll = 1
hero_card = False
hero_card2 = False
hero_card3 = False
hero_card4 = False
hero_card5 = False
hero_card6 = False
hero_card7 = False
hero_card8 = False
hero_card9 = False
hero_card10 = False

#The EventFinder looks at the event lines that are given for a link, and returns a message that is a bit better to read.
def EventFinder(line_type):
	if line_type == 'play':
		return ' play line.'
	elif line_type == 'attack':
		return ' attack line.'
	elif line_type == 'death':
		return ' death line.'
	elif line_type == 'trigger':
		return ' trigger line.'

for comment in comments:
	#This will check each individual comment in a list of comments(for comment in comments).  Comments is the .stream() talked about earlier.
	#Stream only gives the id of the comments, while .body gives the text.  I then had the text encoded in a differnt way than python normally does to avoid errors with non-ASCII characters.
	#All backslashes, commas, and apostrophes are removed to make sure that if a card name is in the comments that it will not be missed because of punctuation.
	#The backslashes on the backslash and apostrophe make it so python reads it as a character and not a special command.
	#All spaces are changed into dashes because the card links use dashes instead of spaces, all characters are also changed into lower case for the same reason.
	#To call the bot both the event and the card need to be surrounded in double parentheses, this is to avoid unintentional callings of the bot and to make finding the cards easier.
	#So I use re.split on text to split all of the text into a list IF it is surrrounded by double parentheses.
	#"If comment.id not in cache" is to prevent the bot from repeatedly replying to the same comment.  At the end of a reply it will store the id of the comment in the cache list.

	#Lets say we had a comment like "Don't you love ((Druid of the Claw))'s ((play)) sound?".  The comment would be changed into "dont-you-love-((druid-of-the-claw))s-((play))-sound".
	#Then it would be split into ["dont-you-love-","druid-of-the-claw","s-","play","-sound"] 
	text = comment.body
	text = text.encode('utf-8','ignore')
	text = text.replace('\\', '')
	text = text.replace(' ','-')
	text = text.replace(',','')
	text = text.replace('\'','')
	text = text.lower()
	comment_list = re.split(r'\(\(|\)\)',text)
	print comment_list
	print text
	if comment.id not in cache:
		#"For card in comment list:"" and "if card in minion list:" work together to check all the entries in comment_list to see if they are a card.
		#If an entry is a card, the bot will then check to see how many responses have already been written "if the_card# =='':" (the bot will only write 10 responses per comment). 
		#Dic_of_grammar is a list of cards that needed to prepared for a response earlier and so they don't need to be redone here, thus the check "if card not in dic_of_grammar".
		#The bot will take unprepared cards and capitalize the start of each word and change the dashes back into spaces. In order to write the card like it is written ingame.
		while True:
			try:
				for card in comment_list:
					if card in dic_of_nicknames:
						card = dic_of_nicknames.get(card)
					if card in minion_list:
						if the_card == '':
							if card not in dic_of_grammar:
								the_card = capwords(card.replace('-',' '))
								#However capwords will also capitalize "the" and "of".
								#To fix this the bot checks if the_card has either "the" or "of" in it by taking each word of the card and making it its own entry in a list using spilt().
								#If any word is equal to "the" or "of", the list gets saved as "the_spliiter".
								#The location of the "the" or "of" in the list is saved inside "replaceindex".  The word is then removed from the_splitter list.
								#The removed word is changed into lowercase and readded at its previous location.
								#After doing this the_card# is made blank then each word in the_splitter is idividually readded into the_card.
		
								#So in our example 'druid-of-the-claw' would be taken from the comment_list, changed into 'Druid Of The Claw', then into ['Druid','Of','The','Claw'].
								#After that into ['Druid','The','Claw'], into ['Druid','of','The','Claw'], into ['Druid','of','Claw'], then into ['Druid','of','the','Claw'], and finally 'Druid of the Claw'
								if 'The' in the_card.split() or 'Of' in the_card.split():
									the_splitter = the_card.split()
									for word in the_splitter:
										if word == 'The':
											replaceindex = the_splitter.index(word)
											the_splitter.remove(word)
											word = word.lower()
											the_splitter.insert(replaceindex,word)
										if word == 'Of':
											replaceindex = the_splitter.index(word)
											the_splitter.remove(word)
											word = word.lower()
											the_splitter.insert(replaceindex,word)
										the_card = ' '.join(the_splitter)
							if card in dic_of_grammar:
								the_card = dic_of_grammar.get(card)
							#This is where the link to hearthhead for any indivdual card is made.  If the card is in dic_of_multiples the link gets a number and a dash added to it.
							#In our example the_card_link would be "http://www.hearthhead.com/cards/druid-of-the-claw". Dic cards would be something like http://www.hearthhead.com/cards/kelthuzad-1
							if card not in dic_of_multiples:
								the_card_link = '%s%s' % (card_link_start,card)
							elif card in dic_of_multiples:
								card = dic_of_multiples.get(card)
								the_card_link = '%s%s' % (card_link_start,card)
						#Everything gets repeated upto 9 more times for any other cards written in the comment.
						elif the_card2 == '':
							if card not in dic_of_grammar:
								the_card2 = capwords(card.replace('-',' '))
								if 'The' in the_card2.split() or 'Of' in the_card2.split():
									the_splitter = the_card2.split()
									for word in the_splitter:
										if word == 'The':
											replaceindex = the_splitter.index(word)
											the_splitter.remove(word)
											word = word.lower()
											the_splitter.insert(replaceindex,word)
										if word == 'Of':
											replaceindex = the_splitter.index(word)
											the_splitter.remove(word)
											word = word.lower()
											the_splitter.insert(replaceindex,word)
										the_card2 = ' '.join(the_splitter)
							if card in dic_of_grammar:
								the_card2 = dic_of_grammar.get(card)
							if card not in dic_of_multiples:
								the_card_link2 = '%s%s' % (card_link_start,card)
							elif card in dic_of_multiples:
								card = dic_of_multiples.get(card)
								the_card_link2 = '%s%s' % (card_link_start,card)
						elif the_card3 == '':
							if card not in dic_of_grammar:
								the_card3 = capwords(card.replace('-',' '))
								if 'The' in the_card3.split() or 'Of' in the_card3.split():
									the_splitter = the_card3.split()
									for word in the_splitter:
										if word == 'The':
											replaceindex = the_splitter.index(word)
											the_splitter.remove(word)
											word = word.lower()
											the_splitter.insert(replaceindex,word)
										if word == 'Of':
											replaceindex = the_splitter.index(word)
											the_splitter.remove(word)
											word = word.lower()
											the_splitter.insert(replaceindex,word)
										the_card3 = ' '.join(the_splitter)
							if card in dic_of_grammar:
								the_card3 = dic_of_grammar.get(card)
							if card not in dic_of_multiples:
								the_card_link3 = '%s%s' % (card_link_start,card)
							elif card in dic_of_multiples:
								card = dic_of_multiples.get(card)
								the_card_link3 = '%s%s' % (card_link_start,card)
						elif the_card4 == '':
							if card not in dic_of_grammar:
								the_card4 = capwords(card.replace('-',' '))
								if 'The' in the_card4.split() or 'Of' in the_card4.split():
									the_splitter = the_card4.split()
									for word in the_splitter:
										if word == 'The':
											replaceindex = the_splitter.index(word)
											the_splitter.remove(word)
											word = word.lower()
											the_splitter.insert(replaceindex,word)
										if word == 'Of':
											replaceindex = the_splitter.index(word)
											the_splitter.remove(word)
											word = word.lower()
											the_splitter.insert(replaceindex,word)
										the_card4 = ' '.join(the_splitter)
							if card in dic_of_grammar:
								the_card4 = dic_of_grammar.get(card)
							if card not in dic_of_multiples:
								the_card_link4 = '%s%s' % (card_link_start,card)
							elif card in dic_of_multiples:
								card = dic_of_multiples.get(card)
								the_card_link4 = '%s%s' % (card_link_start,card)
						elif the_card5 == '':
							if card not in dic_of_grammar:
								the_card5 = capwords(card.replace('-',' '))
								if 'The' in the_card5.split() or 'Of' in the_card5.split():
									the_splitter = the_card5.split()
									for word in the_splitter:
										if word == 'The':
											replaceindex = the_splitter.index(word)
											the_splitter.remove(word)
											word = word.lower()
											the_splitter.insert(replaceindex,word)
										if word == 'Of':
											replaceindex = the_splitter.index(word)
											the_splitter.remove(word)
											word = word.lower()
											the_splitter.insert(replaceindex,word)
										the_card5 = ' '.join(the_splitter)
							if card in dic_of_grammar:
								the_card5 = dic_of_grammar.get(card)
							if card not in dic_of_multiples:
								the_card_link5 = '%s%s' % (card_link_start,card)
							elif card in dic_of_multiples:
								card = dic_of_multiples.get(card)
								the_card_link5 = '%s%s' % (card_link_start,card)
						elif the_card6 == '':
							if card not in dic_of_grammar:
								the_card6 =capwords(card.replace('-',' '))
								if 'The' in the_card6.split() or 'Of' in the_card6.split():
									the_splitter = the_card6.split()
									for word in the_splitter:
										if word == 'The':
											replaceindex = the_splitter.index(word)
											the_splitter.remove(word)
											word = word.lower()
											the_splitter.insert(replaceindex,word)
										if word == 'Of':
											replaceindex = the_splitter.index(word)
											the_splitter.remove(word)
											word = word.lower()
											the_splitter.insert(replaceindex,word)
										the_card6 = ' '.join(the_splitter)
							if card in dic_of_grammar:
								the_card6 = dic_of_grammar.get(card)
							if card not in dic_of_multiples:
								the_card_link6 = '%s%s' % (card_link_start,card)
							elif card in dic_of_multiples:
								card = dic_of_multiples.get(card)
								the_card_link6 = '%s%s' % (card_link_start,card)
						elif the_card7 == '':
							if card not in dic_of_grammar:
								the_card7 = capwords(card.replace('-',' '))
								if 'The' in the_card7.split() or 'Of' in the_card7.split():
									the_splitter = the_card7.split()
									for word in the_splitter:
										if word == 'The':
											replaceindex = the_splitter.index(word)
											the_splitter.remove(word)
											word = word.lower()
											the_splitter.insert(replaceindex,word)
										if word == 'Of':
											replaceindex = the_splitter.index(word)
											the_splitter.remove(word)
											word = word.lower()
											the_splitter.insert(replaceindex,word)
										the_card7 = ' '.join(the_splitter)
							if card in dic_of_grammar:
								the_card7 = dic_of_grammar.get(card)
							if card not in dic_of_multiples:
								the_card_link7 = '%s%s' % (card_link_start,card)
							elif card in dic_of_multiples:
								card = dic_of_multiples.get(card)
								the_card_link7 = '%s%s' % (card_link_start,card)
						elif the_card8 == '':
							if card not in dic_of_grammar:
								the_card8 = capwords(card.replace('-',' '))
								if 'The' in the_card8.split() or 'Of' in the_card8.split():
									the_splitter = the_card8.split()
									for word in the_splitter:
										if word == 'The':
											replaceindex = the_splitter.index(word)
											the_splitter.remove(word)
											word = word.lower()
											the_splitter.insert(replaceindex,word)
										if word == 'Of':
											replaceindex = the_splitter.index(word)
											the_splitter.remove(word)
											word = word.lower()
											the_splitter.insert(replaceindex,word)
										the_card8 = ' '.join(the_splitter)
							if card in dic_of_grammar:
								the_card8 = dic_of_grammar.get(card)
							if card not in dic_of_multiples:
								the_card_link8 = '%s%s' % (card_link_start,card)
							elif card in dic_of_multiples:
								card = dic_of_multiples.get(card)
								the_card_link8 = '%s%s' % (card_link_start,card)
						elif the_card9 == '':
							if card not in dic_of_grammar:
								the_card9 = capwords(card.replace('-',' '))
								if 'The' in the_card9.split() or 'Of' in the_card9.split():
									the_splitter = the_card9.split()
									for word in the_splitter:
										if word == 'The':
											replaceindex = the_splitter.index(word)
											the_splitter.remove(word)
											word = word.lower()
											the_splitter.insert(replaceindex,word)
										if word == 'Of':
											replaceindex = the_splitter.index(word)
											the_splitter.remove(word)
											word = word.lower()
											the_splitter.insert(replaceindex,word)
										the_card9 = ' '.join(the_splitter)
							if card in dic_of_grammar:
								the_card9 = dic_of_grammar.get(card)
							if card not in dic_of_multiples:
								the_card_link9 = '%s%s' % (card_link_start,card)
							elif card in dic_of_multiples:
								card = dic_of_multiples.get(card)
								the_card_link9 = '%s%s' % (card_link_start,card)
						elif the_card10 == '':
							if card not in dic_of_grammar:
								the_card10 = capwords(card.replace('-',' '))
								if 'The' in the_card10.split() or 'Of' in the_card10.split():
									the_splitter = the_card10.split()
									for word in the_splitter:
										if word == 'The':
											replaceindex = the_splitter.index(word)
											the_splitter.remove(word)
											word = word.lower()
											the_splitter.insert(replaceindex,word)
										if word == 'Of':
											replaceindex = the_splitter.index(word)
											the_splitter.remove(word)
											word = word.lower()
											the_splitter.insert(replaceindex,word)
										the_card10 = ' '.join(the_splitter)
							if card in dic_of_grammar:
								the_card10 = dic_of_grammar.get(card)
							if card not in dic_of_multiples:
								the_card_link10 = '%s%s' % (card_link_start,card)
							elif card in dic_of_multiples:
								card = dic_of_multiples.get(card)
								the_card_link10 = '%s%s' % (card_link_start,card)
					if card not in minion_list:
						for hero in list_of_hero_names:
							if card == hero:
								if the_card == '':
									the_card = capwords(hero)
									hero_card = True
								elif the_card2 == '':
									the_card2 = capwords(hero)
									hero_card2 = True
								elif the_card3 == '':
									the_card3 = capwords(hero)
									hero_card3 = True
								elif the_card4 == '':
									the_card4 = capwords(hero)
									hero_card4 = True
								elif the_card5 == '':
									the_card5 = capwords(hero)
									hero_card5 = True
								elif the_card6 == '':
									the_card6 = capwords(hero)
									hero_card6 = True
								elif the_card7 == '':
									the_card7 = capwords(hero)
									hero_card7 = True
								elif the_card8 == '':
									the_card8 = capwords(hero)
									hero_card8 = True
								elif the_card9 == '':
									the_card9 = capwords(hero)
									hero_card9 = True
								elif the_card10 == '':
									the_card10 = capwords(hero)
									hero_card10 = True
				#This searches for through the comment for any events the same way the cards were searched for.  It then uses the event_caller to dress up the message a bit.
				#In the example I stated earlier 'play' would be found in the list and have event finder return "\'s play line".
				for line in comment_list:
					if line in event_list:
						if the_event == '':
							the_event = line
							event_caller = EventFinder(the_event)
						elif the_event2 == '':
							the_event2 = line
							event_caller2 = EventFinder(the_event2)
						elif the_event3 == '':
							the_event3 = line 
							event_caller3 = EventFinder(the_event3)
						elif the_event4 == '':
							the_event4 = line 
							event_caller4 = EventFinder(the_event4)
						elif the_event5 == '':
							the_event5 = line 
							event_caller5 = EventFinder(the_event5)
						elif the_event6 == '':
							the_event6 = line 
							event_caller6 = EventFinder(the_event6)
						elif the_event7 == '':
							the_event7 = line 
							event_caller7 = EventFinder(the_event7)
						elif the_event8 == '':
							the_event8 = line 
							event_caller8 = EventFinder(the_event8)
						elif the_event9 == '':
							the_event9 = line 
							event_caller9 = EventFinder(the_event9)
						elif the_event10 == '':
							the_event10 = line 
							event_caller10 = EventFinder(the_event10)	
					if line not in event_list:
						if the_card.lower() in list_of_hero_names and the_event == '':
							entry_pos = list_of_hero_names.index(the_card.lower())
							for entry in list_of_heroes[entry_pos].keys():
								if line == entry:
										the_event = entry.replace('-', ' ')
										the_result = list_of_heroes[entry_pos].get(entry)
						elif the_card2.lower() in list_of_hero_names and the_event2 == '':
							entry_pos = list_of_hero_names.index(the_card2.lower())
							for entry in list_of_heroes[entry_pos].keys():
								if line == entry:
										the_event2 = entry.replace('-', ' ')
										the_result2 = list_of_heroes[entry_pos].get(entry)
						elif the_card3.lower() in list_of_hero_names and the_event3 == '':
							entry_pos = list_of_hero_names.index(the_card3.lower())
							for entry in list_of_heroes[entry_pos].keys():
								if line == entry:
										the_event3 = entry.replace('-', ' ')
										the_result3 = list_of_heroes[entry_pos].get(entry)
						elif the_card4.lower() in list_of_hero_names and the_event4 == '':
							entry_pos = list_of_hero_names.index(the_card4.lower())
							for entry in list_of_heroes[entry_pos].keys():
								if line == entry:
										the_event4 = entry.replace('-', ' ')
										the_result4 = list_of_heroes[entry_pos].get(entry)
						elif the_card5.lower() in list_of_hero_names and the_event5 == '':
							entry_pos = list_of_hero_names.index(the_card5.lower())
							for entry in list_of_heroes[entry_pos].keys():
								if line == entry:
										the_event5 = entry.replace('-', ' ')
										the_result5 = list_of_heroes[entry_pos].get(entry)
						elif the_card6.lower() in list_of_hero_names and the_event6 == '':
							entry_pos = list_of_hero_names.index(the_card6.lower())
							for entry in list_of_heroes[entry_pos].keys():
								if line == entry:
										the_event6 = entry.replace('-', ' ')
										the_result6 = list_of_heroes[entry_pos].get(entry)
						elif the_card7.lower() in list_of_hero_names and the_event7 == '':
							entry_pos = list_of_hero_names.index(the_card7.lower())
							for entry in list_of_heroes[entry_pos].keys():
								if line == entry:
										the_event7 = entry.replace('-', ' ')
										the_result7 = list_of_heroes[entry_pos].get(entry)
						elif the_card8.lower() in list_of_hero_names and the_event8 == '':
							entry_pos = list_of_hero_names.index(the_card8.lower())
							for entry in list_of_heroes[entry_pos].keys():
								if line == entry:
										the_event8 = entry.replace('-', ' ')
										the_result8 = list_of_heroes[entry_pos].get(entry)
						elif the_card9.lower() in list_of_hero_names and the_event9 == '':
							entry_pos = list_of_hero_names.index(the_card9.lower())
							for entry in list_of_heroes[entry_pos].keys():
								if line == entry:
										the_event9 = entry.replace('-', ' ')
										the_result9 = list_of_heroes[entry_pos].get(entry)
						elif the_card10.lower() in list_of_hero_names and the_event10 == '':
							entry_pos = list_of_hero_names.index(the_card10.lower())
							for entry in list_of_heroes[entry_pos].keys():
								if line == entry:
										the_event10 = entry.replace('-', ' ')
										the_result10 = list_of_heroes[entry_pos].get(entry)
						for hero in nefarian_plays.keys():
							if 'play-%s' % (hero) == line:
								if the_event == '':
									the_event = nefarian_plays.get(hero)
									event_caller = ' play line against %s.' % (hero)
								elif the_event2 == '':
									the_event2 = nefarian_plays.get(hero)
									event_caller2 = ' play line against %s.' % (hero)
								elif the_event3 == '':
									the_event3 = nefarian_plays.get(hero)
									event_caller3 = ' play line against %s.' % (hero)
								elif the_event4 == '':
									the_event4 = nefarian_plays.get(hero)
									event_caller4 = ' play line against %s.' % (hero)
								elif the_event5 == '':
									the_event5 = nefarian_plays.get(hero)
									event_caller5 = ' play line against %s.' % (hero)
								elif the_event6 == '':
									the_event6 = nefarian_plays.get(hero) 
									event_caller6 = ' play line against %s.' % (hero)
								elif the_event7 == '':
									the_event7 = nefarian_plays.get(hero)
									event_caller7 = ' play line against %s.' % (hero)
								elif the_event8 == '':
									the_event8 = nefarian_plays.get(hero) 
									event_caller8 = ' play line against %s.' % (hero)
								elif the_event9 == '':
									the_event9 = nefarian_plays.get(hero) 
									event_caller9 = ' play line against %s.' % (hero)
								elif the_event10 == '':
									the_event10 = nefarian_plays.get(hero) 
									event_caller10 = ' play line against %s.' % (hero)
						for i in range(0,11):
							if line == 'trigger%s' % (i):
								if the_event == '':
									the_event = cthun_triggers[i]
									event_caller = EventFinder('trigger')
								elif the_event2 == '':
									the_event2 = cthun_triggers[i]
									event_caller2 = EventFinder('trigger') 
								elif the_event3 == '':
									the_event3 = cthun_triggers[i]
									event_caller3 = EventFinder('trigger') 
								elif the_event4 == '':
									the_event4 = cthun_triggers[i]
									event_caller4 = EventFinder('trigger') 
								elif the_event5 == '':
									the_event5 = cthun_triggers[i]
									event_caller5 = EventFinder('trigger') 
								elif the_event6 == '':
									the_event6 = cthun_triggers[i]
									event_caller6 = EventFinder('trigger') 
								elif the_event7 == '':
									the_event7 = cthun_triggers[i]
									event_caller7 = EventFinder('trigger') 
								elif the_event8 == '':
									the_event8 = cthun_triggers[i]
									event_caller8 = EventFinder('trigger') 
								elif the_event9 == '':
									the_event9 = cthun_triggers[i]
									event_caller9 = EventFinder('trigger') 
								elif the_event10 == '':
									the_event10 = cthun_triggers[i]
									event_caller10 = EventFinder('trigger')
						if line == 'play-2' or line == 'alternate':
							if the_event == '':
								the_event = 'alternate'
								event_caller = ' alternate play line.'
							if the_event2 == '':
								the_event2 = 'alternate'
								event_caller2 = ' alternate play line.'
							if the_event3 == '':
								the_event3 = 'alternate'
								event_caller3 = ' alternate play line.' 
							if the_event4 == '':
								the_event4 = 'alternate'
								event_caller4 = ' alternate play line.'
							if the_event5 == '':
								the_event5 = 'alternate'
								event_caller5 = ' alternate play line.' 
							if the_event6 == '':
								the_event6 = 'alternate'
								event_caller6 = ' alternate play line.' 
							if the_event7 == '':
								the_event7 = 'alternate'
								event_caller7 = ' alternate play line.' 
							if the_event8 == '':
								the_event8 = cthun_triggers[i]
								event_caller8 = ' alternate play line.' 
							if the_event9 == '':
								the_event9 = 'alternate'
								event_caller9 = ' alternate play line.'
							if the_event9 == '':
								the_event10 = 'alternate'
								event_caller10 = ' alternate play line.'
				#This is where the  message is made.  If both events and cards are not empty it will start making the message.  I used ifs instead of elifs, because elifs will only work once.
				#First it will find the link to the sound with SoundFinder.  #Then it will take the card's name, message about the type of line, and the link itself.
				#It is formatted into []() which is Reddit's way of having hyperlinks in comments.
				#In our example the_result would be "http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_EX1_165_Play_01.ogg" and then "Druid of the Claw's [play line.](the_result)" 
				if the_card != '' and the_event != '' and hero_card == False:
					if the_card not in list_of_exceptions:
						the_result = SoundFinder(the_card_link,the_event)
					elif the_card in list_of_exceptions:
						if the_card == 'C\'thun':
							if the_event == 'trigger':
								dice_roll = randint(0,11)
								the_result = '%s%s' % (audio_link_start, cthun_triggers[dice_roll])
							for i in range(0,11):
								if the_event == cthun_triggers[i]:
									the_result = '%s%s' % (audio_link_start,the_event)
								elif i == 11:
									the_result = SoundFinder(the_card_link,the_event)
						elif the_card == 'Y\'Shaarj, Rage Unbound':
							if the_event == 'play':
								the_result = '%s/hs/sounds/enus/VO_OG_133_Male_OldGod_Play_01.ogg' % (audio_link_start)
							if the_event == 'attack':
								the_result = '%shs/sounds/enus/VO_OG_133_Male_OldGod_Attack_01.ogg' % (audio_link_start)
							if the_event == 'death':
								the_result = '%s/hs/sounds/enus/VO_OG_133_Male_OldGod_Death_01.ogg' % (audio_link_start)
						elif the_card == 'N\'zoth, the Corruptor':
							if the_event == 'play':
								the_result = '%s/hs/sounds/enus/VO_OG_042_Male_OldGod_Play_01.ogg' % (audio_link_start)
							if the_event == 'attack':
								the_result = '%s/hs/sounds/enus/VO_OG_042_Male_OldGod_Attack_01.ogg' % (audio_link_start)
							if the_event == 'death':
								the_result = '%s/hs/sounds/enus/VO_OG_042_Male_OldGod_Death_01.ogg' % (audio_link_start)
						elif the_card == 'Nefarian':
							if the_event == 'death' or the_event == 'attack':
								the_result = SoundFinder(the_card_link,the_event)
							else:
								the_result = '%s%s' % (audio_link_start,the_event)
						elif the_card == 'Rend Blackhand':
							if the_event == 'play':
								the_result = '%s/hs/sounds/enus/VO_BRMA09_1_START_01.ogg' % (audio_link_start)
							if the_event == 'attack':
								the_result = '%s/hs/sounds/enus/VO_BRMA09_1_RESPONSE_04.ogg' % (audio_link_start)
							if the_event == 'death':
								the_result = SoundFinder(the_card_link,the_event)
						elif the_card == 'Emperor Thaurissan':
							if the_event == 'play':
								the_result = '%s/hs/sounds/enus/VO_BRMA03_1_CARD_04.ogg' % (audio_link_start)
							if the_event == 'attack':
								the_result = '%s/hs/sounds/enus/VO_BRMA03_1_HERO_POWER_06.ogg' % (audio_link_start)
							if the_event == 'death':
								the_result = SoundFinder(the_card_link,the_event)
						elif the_card == 'Majordomo Executus':
							if the_event == 'play':
								the_result = '/hs/sounds/enus/VO_BRMA06_1_START_01.ogg' % (audio_link_start)
							if the_event == 'attack':
								the_result = '%s/hs/sounds/enus/VO_BRMA06_1_TURN1_02_ALT.ogg' % (audio_link_start)
							if the_event == 'death':
								the_result = SoundFinder(the_card_link,the_event)
					if the_result != None:
						the_reply = '''* %s\'s[%s](%s)	
		
		
''' % (the_card, event_caller, the_result)
						print the_reply
				if the_card != '' and the_event != '' and hero_card == True:
					if the_result != None:
						the_reply = '''* %s\'s [%s line.](%s) 
		
		
''' % (the_card, the_event, the_result)
					print the_reply
				if the_card2 != '' and the_event2 != '' and hero_card2 == False:
					if the_card2 not in list_of_exceptions:
						the_result2 = SoundFinder(the_card_link2,the_event2)
					elif the_card2 in list_of_exceptions:
						if the_card2 == 'C\'thun':
							if the_event2 == 'trigger':
								dice_roll = randint(0,11)
								the_result2 = '%s%s' % (audio_link_start, cthun_triggers[dice_roll])
							for i in range(0,11):
								if the_event2 == cthun_triggers[i]:
									the_result2 = '%s%s' % (audio_link_start,the_event2)
								elif i == 11:
									the_result2 = SoundFinder(the_card_link2,the_event2)
						elif the_card2 == 'Y\'Shaarj, Rage Unbound':
							if the_event2 == 'play':
								the_result2 = '%s/hs/sounds/enus/VO_OG_133_Male_OldGod_Play_01.ogg' % (audio_link_start)
							if the_event2 == 'attack':
								the_result2 = '%shs/sounds/enus/VO_OG_133_Male_OldGod_Attack_01.ogg' % (audio_link_start)
							if the_event2 == 'death':
								the_result2 = '%s/hs/sounds/enus/VO_OG_133_Male_OldGod_Death_01.ogg' % (audio_link_start)
						elif the_card2 == 'N\'zoth, the Corruptor':
							if the_event2 == 'play':
								the_result2 = '%s/hs/sounds/enus/VO_OG_042_Male_OldGod_Play_01.ogg' % (audio_link_start)
							if the_event2 == 'attack':
								the_result2 = '%s/hs/sounds/enus/VO_OG_042_Male_OldGod_Attack_01.ogg' % (audio_link_start)
							if the_event2 == 'death':
								the_result2 = '%s/hs/sounds/enus/VO_OG_042_Male_OldGod_Death_01.ogg' % (audio_link_start)
						elif the_card2 == 'Nefarian':
							if the_event2 == 'death' or the_event2 == 'attack':
								the_result2 = SoundFinder(the_card_link2,the_event2)
							else:
								the_result2 = '%s%s' % (audio_link_start,the_event2)
						elif the_card2 == 'Rend Blackhand':
							if the_event2 == 'play':
								the_result2 = '%s/hs/sounds/enus/VO_BRMA09_1_START_01.ogg' % (audio_link_start)
							if the_event2 == 'attack':
								the_result2 = '%s/hs/sounds/enus/VO_BRMA09_1_RESPONSE_04.ogg' % (audio_link_start)
							if the_event2 == 'death':
								the_result2 = SoundFinder(the_card_link2,the_event2)
						elif the_card2 == 'Emperor Thaurissan':
							if the_event2 == 'play':
								the_result2 = '%s/hs/sounds/enus/VO_BRMA03_1_CARD_04.ogg' % (audio_link_start)
							if the_event2 == 'attack':
								the_result2 = '%s/hs/sounds/enus/VO_BRMA03_1_HERO_POWER_06.ogg' % (audio_link_start)
							if the_event2 == 'death':
								the_result2 = SoundFinder(the_card_link2,the_event2)
						elif the_card2 == 'Majordomo Executus':
							if the_event2 == 'play':
								the_result2 = '%s/hs/sounds/enus/VO_BRMA06_1_START_01.ogg' % (audio_link_start)
							if the_event2 == 'attack':
								the_result2 = '%s/hs/sounds/enus/VO_BRMA06_1_TURN1_02_ALT.ogg' % (audio_link_start)
							if the_event2 == 'death':
								the_result2 = SoundFinder(the_card_link2,the_event2)
					if the_result2 != None:
						the_reply2 = '''* %s\'s[%s](%s)
		
		
''' % (the_card2, event_caller2, the_result2)
						print the_reply2
				if the_card2 != '' and the_event2 != '' and hero_card2 == True:
					if the_result2 != None:
						the_reply2 = '''* %s\'s [%s line.](%s) 
		
		
''' % (the_card2, the_event2, the_result2)
					print the_reply2
				if the_card3 != '' and the_event3 != '' and hero_card3 == False:
					if the_card3 not in list_of_exceptions:
						the_result3 = SoundFinder(the_card_link3,the_event3)
					elif the_card3 in list_of_exceptions:
						if the_card3 == 'C\'thun':
							if the_event3 == 'trigger':
								dice_roll = randint(0,11)
								the_result3 = '%s%s' % (audio_link_start, cthun_triggers[dice_roll])
							for i in range(0,11):
								if the_event3 == cthun_triggers[i]:
									the_result3 = '%s%s' % (audio_link_start,the_event3)
								elif i == 11:
									the_result3 = SoundFinder(the_card_link3,the_event3)
						elif the_card3 == 'Y\'Shaarj, Rage Unbound':
							if the_event3 == 'play':
								the_result3 = '%s/hs/sounds/enus/VO_OG_133_Male_OldGod_Play_01.ogg' % (audio_link_start)
							if the_event3 == 'attack':
								the_result3 = '%shs/sounds/enus/VO_OG_133_Male_OldGod_Attack_01.ogg' % (audio_link_start)
							if the_event3 == 'death':
								the_result3 = '%s/hs/sounds/enus/VO_OG_133_Male_OldGod_Death_01.ogg' % (audio_link_start)
						elif the_card3 == 'N\'zoth, the Corruptor':
							if the_event3 == 'play':
								the_result3 = '%s/hs/sounds/enus/VO_OG_042_Male_OldGod_Play_01.ogg' % (audio_link_start)
							if the_event3 == 'attack':
								the_result3 = '%s/hs/sounds/enus/VO_OG_042_Male_OldGod_Attack_01.ogg' % (audio_link_start)
							if the_event3 == 'death':
								the_result3 = '%s/hs/sounds/enus/VO_OG_042_Male_OldGod_Death_01.ogg' % (audio_link_start)
						elif the_card3 == 'Nefarian':
							if the_event3 == 'death' or the_event3 == 'attack':
								the_result3 = SoundFinder(the_card_link3,the_event3)
							else:
								the_result3 = '%s%s' % (audio_link_start,the_event3)
						elif the_card3 == 'Rend Blackhand':
							if the_event3 == 'play':
								the_result3 = '%s/hs/sounds/enus/VO_BRMA09_1_START_01.ogg' % (audio_link_start)
							if the_event3 == 'attack':
								the_result3 = '%s/hs/sounds/enus/VO_BRMA09_1_RESPONSE_04.ogg' % (audio_link_start)
							if the_event3 == 'death':
								the_result3 = SoundFinder(the_card_link3,the_event3)
						elif the_card3 == 'Emperor Thaurissan':
							if the_event3 == 'play':
								the_result3 = '%s/hs/sounds/enus/VO_BRMA03_1_CARD_04.ogg' % (audio_link_start)
							if the_event3 == 'attack':
								the_result3 = '%s/hs/sounds/enus/VO_BRMA03_1_HERO_POWER_06.ogg' % (audio_link_start)
							if the_event3 == 'death':
								the_result3 = SoundFinder(the_card_link3,the_event3)
						elif the_card3 == 'Majordomo Executus':
							if the_event3 == 'play':
								the_result3 = '%s/hs/sounds/enus/VO_BRMA06_1_START_01.ogg' % (audio_link_start)
							if the_event3 == 'attack':
								the_result3 = '%s/hs/sounds/enus/VO_BRMA06_1_TURN1_02_ALT.ogg' % (audio_link_start)
							if the_event3 == 'death':
								the_result3 = SoundFinder(the_card_link3,the_event3)
					if the_result3 != None:
						the_reply3 = '''* %s\'s[%s](%s)
		
		
''' % (the_card3, event_caller3, the_result3)
						print the_reply3
				if the_card3 != '' and the_event3 != '' and hero_card3 == True:
					if the_result3 != None:
						the_reply3 = '''* %s\'s [%s line.](%s) 
		
		
''' % (the_card3, the_event3, the_result3)
					print the_reply3
				if the_card4 != '' and the_event4 != '' and hero_card4 == False:
					if the_card4 not in list_of_exceptions:
						the_result4 = SoundFinder(the_card_link4,the_event4)
					elif the_card4 in list_of_exceptions:
						if the_card4 == 'C\'thun':
							if the_event4 == 'trigger':
								dice_roll = randint(0,11)
								the_result4 = '%s%s' % (audio_link_start, cthun_triggers[dice_roll])
							for i in range(0,11):
								if the_event4 == cthun_triggers[i]:
									the_result4 = '%s%s' % (audio_link_start,the_event4)
								elif i == 11:
									the_result4 = SoundFinder(the_card_link4,the_event4)
						elif the_card4 == 'Y\'Shaarj, Rage Unbound':
							if the_event4 == 'play':
								the_result4 = '%s/hs/sounds/enus/VO_OG_133_Male_OldGod_Play_01.ogg' % (audio_link_start)
							if the_event4 == 'attack':
								the_result4 = '%shs/sounds/enus/VO_OG_133_Male_OldGod_Attack_01.ogg' % (audio_link_start)
							if the_event4 == 'death':
								the_result4 = '%s/hs/sounds/enus/VO_OG_133_Male_OldGod_Death_01.ogg' % (audio_link_start)
						elif the_card4 == 'N\'zoth, the Corruptor':
							if the_event4 == 'play':
								the_result4 = '%s/hs/sounds/enus/VO_OG_042_Male_OldGod_Play_01.ogg' % (audio_link_start)
							if the_event4 == 'attack':
								the_result4 = '%s/hs/sounds/enus/VO_OG_042_Male_OldGod_Attack_01.ogg' % (audio_link_start)
							if the_event4 == 'death':
								the_result4 = '%s/hs/sounds/enus/VO_OG_042_Male_OldGod_Death_01.ogg' % (audio_link_start)
						elif the_card4 == 'Nefarian':
							if the_event4 == 'death' or the_event4 == 'attack':
								the_result4 = SoundFinder(the_card_link4,the_event4)
							else:
								the_result4 = '%s%s' % (audio_link_start,the_event4)
						elif the_card4 == 'Rend Blackhand':
							if the_event4 == 'play':
								the_result4 = '%s/hs/sounds/enus/VO_BRMA09_1_START_01.ogg' % (audio_link_start)
							if the_event4 == 'attack':
								the_result4 = '%s/hs/sounds/enus/VO_BRMA09_1_RESPONSE_04.ogg' % (audio_link_start)
							if the_event4 == 'death':
								the_result4 = SoundFinder(the_card_link4,the_event4)
						elif the_card4 == 'Emperor Thaurissan':
							if the_event4 == 'play':
								the_result4 = '%s/hs/sounds/enus/VO_BRMA03_1_CARD_04.ogg' % (audio_link_start)
							if the_event4 == 'attack':
								the_result4 = '%s/hs/sounds/enus/VO_BRMA03_1_HERO_POWER_06.ogg' % (audio_link_start)
							if the_event4 == 'death':
								the_result4 = SoundFinder(the_card_link4,the_event4)
						elif the_card4 == 'Majordomo Executus':
							if the_event4 == 'play':
								the_result4 = '%s/hs/sounds/enus/VO_BRMA06_1_START_01.ogg' % (audio_link_start)
							if the_event4 == 'attack':
								the_result4 = '%s/hs/sounds/enus/VO_BRMA06_1_TURN1_02_ALT.ogg' % (audio_link_start)
							if the_event4 == 'death':
								the_result4 = SoundFinder(the_card_link4,the_event4)
					if the_result4 != None:
						the_reply4 = '''* %s\'s[%s](%s)
		
		
''' % (the_card4, event_caller4, the_result4)
						print the_reply4
				if the_card4 != '' and the_event4 != '' and hero_card4 == True:
					if the_result4 != None:
						the_reply4 = '''* %s\'s [%s line.](%s) 
		
		
''' % (the_card4, the_event4, the_result4)
					print the_reply4
				if the_card5 != '' and the_event5 != '' and hero_card5 == False:
					if the_card5 not in list_of_exceptions:
						the_result5 = SoundFinder(the_card_link5,the_event5)
					elif the_card5 in list_of_exceptions:
						if the_card5 == 'C\'thun':
							if the_event5 == 'trigger':
								dice_roll = randint(0,11)
								the_result5 = '%s%s' % (audio_link_start, cthun_triggers[dice_roll])
							for i in range(0,11):
								if the_event5 == cthun_triggers[i]:
									the_result5 = '%s%s' % (audio_link_start,the_event5)
								elif i == 11:
									the_result5 = SoundFinder(the_card_link5,the_event5)
						elif the_card5 == 'Y\'Shaarj, Rage Unbound':
							if the_event5 == 'play':
								the_result5 = '%s/hs/sounds/enus/VO_OG_133_Male_OldGod_Play_01.ogg' % (audio_link_start)
							if the_event5 == 'attack':
								the_result5 = '%shs/sounds/enus/VO_OG_133_Male_OldGod_Attack_01.ogg' % (audio_link_start)
							if the_event5 == 'death':
								the_result5 = '%s/hs/sounds/enus/VO_OG_133_Male_OldGod_Death_01.ogg' % (audio_link_start)
						elif the_card5 == 'N\'zoth, the Corruptor':
							if the_event5 == 'play':
								the_result5 = '%s/hs/sounds/enus/VO_OG_042_Male_OldGod_Play_01.ogg' % (audio_link_start)
							if the_event5 == 'attack':
								the_result5 = '%s/hs/sounds/enus/VO_OG_042_Male_OldGod_Attack_01.ogg' % (audio_link_start)
							if the_event5 == 'death':
								the_result5 = '%s/hs/sounds/enus/VO_OG_042_Male_OldGod_Death_01.ogg' % (audio_link_start)
						elif the_card5 == 'Nefarian':
							if the_event5 == 'death' or the_event5 == 'attack':
								the_result5 = SoundFinder(the_card_link5,the_event5)
							else:
								the_result5 = '%s%s' % (audio_link_start,the_event5)
						elif the_card5 == 'Rend Blackhand':
							if the_event5 == 'play':
								the_result5 = '%s/hs/sounds/enus/VO_BRMA09_1_START_01.ogg' % (audio_link_start)
							if the_event5 == 'attack':
								the_result5 = '%s/hs/sounds/enus/VO_BRMA09_1_RESPONSE_04.ogg' % (audio_link_start)
							if the_event5 == 'death':
								the_result5 = SoundFinder(the_card_link5,the_event5)
						elif the_card5 == 'Emperor Thaurissan':
							if the_event5 == 'play':
								the_result5 = '%s/hs/sounds/enus/VO_BRMA03_1_CARD_04.ogg' % (audio_link_start)
							if the_event5 == 'attack':
								the_result5 = '%s/hs/sounds/enus/VO_BRMA03_1_HERO_POWER_06.ogg' % (audio_link_start)
							if the_event5 == 'death':
								the_result5 = SoundFinder(the_card_link5,the_event5)
						elif the_card5 == 'Majordomo Executus':
							if the_event5 == 'play':
								the_result5 = '%s/hs/sounds/enus/VO_BRMA06_1_START_01.ogg' % (audio_link_start)
							if the_event5 == 'attack':
								the_result5 = '%s/hs/sounds/enus/VO_BRMA06_1_TURN1_02_ALT.ogg' % (audio_link_start)
							if the_event5 == 'death':
								the_result5 = SoundFinder(the_card_link5,the_event5)
					if the_result5 != None:
						the_reply5 = '''* %s\'s[%s](%s)
		
		
''' % (the_card5, event_caller5, the_result5)
						print the_reply5
				if the_card5 != '' and the_event5 != '' and hero_card5 == True:
					if the_result5 != None:
						the_reply5 = '''* %s\'s [%s line.](%s) 
		
		
''' % (the_card5, the_event5, the_result5)
					print the_reply5
				if the_card6 != '' and the_event6 != '' and hero_card6 == False:
					if the_card6 not in list_of_exceptions:
						the_result6 = SoundFinder(the_card_link6,the_event6)
					elif the_card6 in list_of_exceptions:
						if the_card6 == 'C\'thun':
							if the_event6 == 'trigger':
								dice_roll = randint(0,11)
								the_result6 = '%s%s' % (audio_link_start, cthun_triggers[dice_roll])
							for i in range(0,11):
								if the_event6 == cthun_triggers[i]:
									the_result6 = '%s%s' % (audio_link_start,the_event6)
								elif i == 11:
									the_result6 = SoundFinder(the_card_link6,the_event6)
						elif the_card6 == 'Y\'Shaarj, Rage Unbound':
							if the_event6 == 'play':
								the_result6 = '%s/hs/sounds/enus/VO_OG_133_Male_OldGod_Play_01.ogg' % (audio_link_start)
							if the_event6 == 'attack':
								the_result6 = '%shs/sounds/enus/VO_OG_133_Male_OldGod_Attack_01.ogg' % (audio_link_start)
							if the_event6 == 'death':
								the_result6 = '%s/hs/sounds/enus/VO_OG_133_Male_OldGod_Death_01.ogg' % (audio_link_start)
						elif the_card6 == 'N\'zoth, the Corruptor':
							if the_event6 == 'play':
								the_result6 = '%s/hs/sounds/enus/VO_OG_042_Male_OldGod_Play_01.ogg' % (audio_link_start)
							if the_event6 == 'attack':
								the_result6 = '%s/hs/sounds/enus/VO_OG_042_Male_OldGod_Attack_01.ogg' % (audio_link_start)
							if the_event6 == 'death':
								the_result6 = '%s/hs/sounds/enus/VO_OG_042_Male_OldGod_Death_01.ogg' % (audio_link_start)
						elif the_card6 == 'Nefarian':
							if the_event6 == 'death' or the_event6 == 'attack':
								the_result6 = SoundFinder(the_card_link6,the_event6)
							else:
								the_result6 = '%s%s' % (audio_link_start,the_event6)
						elif the_card6 == 'Rend Blackhand':
							if the_event6 == 'play':
								the_result6 = '%s/hs/sounds/enus/VO_BRMA09_1_START_01.ogg' % (audio_link_start)
							if the_event6 == 'attack':
								the_result6 = '%s/hs/sounds/enus/VO_BRMA09_1_RESPONSE_04.ogg' % (audio_link_start)
							if the_event6 == 'death':
								the_result6 = SoundFinder(the_card_link6,the_event6)
						elif the_card6 == 'Emperor Thaurissan':
							if the_event6 == 'play':
								the_result6 = '%s/hs/sounds/enus/VO_BRMA03_1_CARD_04.ogg' % (audio_link_start)
							if the_event6 == 'attack':
								the_result6 = '%s/hs/sounds/enus/VO_BRMA03_1_HERO_POWER_06.ogg' % (audio_link_start)
							if the_event6 == 'death':
								the_result6 = SoundFinder(the_card_link6,the_event6)
						elif the_card6 == 'Majordomo Executus':
							if the_event6 == 'play':
								the_result6 = '%s/hs/sounds/enus/VO_BRMA06_1_START_01.ogg' % (audio_link_start)
							if the_event6 == 'attack':
								the_result6 = '%s/hs/sounds/enus/VO_BRMA06_1_TURN1_02_ALT.ogg' % (audio_link_start)
							if the_event6 == 'death':
								the_result6 = SoundFinder(the_card_link6,the_event6)
					if the_result6 != None:
						the_reply6 = '''* %s\'s[%s](%s)
		
		
''' % (the_card6, event_caller6, the_result6)
						print the_reply6
				if the_card6 != '' and the_event6 != '' and hero_card6 == True:
					if the_result6 != None:
						the_reply6 = '''* %s\'s [%s line.](%s) 
		
		
''' % (the_card6, the_event6, the_result6)
					print the_reply6
				if the_card7 != '' and the_event7 != '' and hero_card7 == False:
					if the_card7 not in list_of_exceptions:
						the_result7 = SoundFinder(the_card_link7,the_event7)
					elif the_card7 in list_of_exceptions:
						if the_card7 == 'C\'thun':
							if the_event7 == 'trigger':
								dice_roll = randint(0,11)
								the_result7 = '%s%s' % (audio_link_start, cthun_triggers[dice_roll])
							for i in range(0,11):
								if the_event7 == cthun_triggers[i]:
									the_result7 = '%s%s' % (audio_link_start,the_event7)
								elif i == 11:
									the_result7 = SoundFinder(the_card_link7,the_event7)
						elif the_card7 == 'Y\'Shaarj, Rage Unbound':
							if the_event7 == 'play':
								the_result7 = '%s/hs/sounds/enus/VO_OG_133_Male_OldGod_Play_01.ogg' % (audio_link_start)
							if the_event7 == 'attack':
								the_result7 = '%shs/sounds/enus/VO_OG_133_Male_OldGod_Attack_01.ogg' % (audio_link_start)
							if the_event7 == 'death':
								the_result7 = '%s/hs/sounds/enus/VO_OG_133_Male_OldGod_Death_01.ogg' % (audio_link_start)
						elif the_card7 == 'N\'zoth, the Corruptor':
							if the_event7 == 'play':
								the_result7 = '%s/hs/sounds/enus/VO_OG_042_Male_OldGod_Play_01.ogg' % (audio_link_start)
							if the_event7 == 'attack':
								the_result7 = '%s/hs/sounds/enus/VO_OG_042_Male_OldGod_Attack_01.ogg' % (audio_link_start)
							if the_event7 == 'death':
								the_result7 = '%s/hs/sounds/enus/VO_OG_042_Male_OldGod_Death_01.ogg' % (audio_link_start)
						elif the_card7 == 'Nefarian':
							if the_event7 == 'death' or the_event7 == 'attack':
								the_result7 = SoundFinder(the_card_link7,the_event7)
							else:
								the_result7 = '%s%s' % (audio_link_start,the_event7)
						elif the_card7 == 'Rend Blackhand':
							if the_event7 == 'play':
								the_result7 = '%s/hs/sounds/enus/VO_BRMA09_1_START_01.ogg' % (audio_link_start)
							if the_event7 == 'attack':
								the_result7 = '%s/hs/sounds/enus/VO_BRMA09_1_RESPONSE_04.ogg' % (audio_link_start)
							if the_event7 == 'death':
								the_result7 = SoundFinder(the_card_link7,the_event7)
						elif the_card7 == 'Emperor Thaurissan':
							if the_event7 == 'play':
								the_result7 = '%s/hs/sounds/enus/VO_BRMA03_1_CARD_04.ogg' % (audio_link_start)
							if the_event7 == 'attack':
								the_result7 = '%s/hs/sounds/enus/VO_BRMA03_1_HERO_POWER_06.ogg' % (audio_link_start)
							if the_event7 == 'death':
								the_result7 = SoundFinder(the_card_link7,the_event7)
						elif the_card7 == 'Majordomo Executus':
							if the_event7 == 'play':
								the_result7 = '%s/hs/sounds/enus/VO_BRMA06_1_START_01.ogg' % (audio_link_start)
							if the_event7 == 'attack':
								the_result7 = '%s/hs/sounds/enus/VO_BRMA06_1_TURN1_02_ALT.ogg' % (audio_link_start)
							if the_event7 == 'death':
								the_result7 = SoundFinder(the_card_link7,the_event7)
					if the_result7 != None:
						the_reply7 = '''* %s\'s[%s](%s)
		
		
''' % (the_card7, event_caller7, the_result7)
						print the_reply7
				if the_card7 != '' and the_event7 != '' and hero_card7 == True:
					if the_result7 != None:
						the_reply7 = '''* %s\'s [%s line.](%s) 
		
		
''' % (the_card7, the_event7, the_result7)
					print the_reply7
				if the_card8 != '' and the_event8 != '' and hero_card8 == False:
					if the_card8 not in list_of_exceptions:
						the_result8 = SoundFinder(the_card_link8,the_event8)
					elif the_card8 in list_of_exceptions:
						if the_card8 == 'C\'thun':
							if the_event8 == 'trigger':
								dice_roll = randint(0,11)
								the_result8 = '%s%s' % (audio_link_start, cthun_triggers[dice_roll])
							for i in range(0,11):
								if the_event8 == cthun_triggers[i]:
									the_result8 = '%s%s' % (audio_link_start,the_event8)
								elif i == 11:
									the_result8 = SoundFinder(the_card_link8,the_event8)
						elif the_card8 == 'Y\'Shaarj, Rage Unbound':
							if the_event8 == 'play':
								the_result8 = '%s/hs/sounds/enus/VO_OG_133_Male_OldGod_Play_01.ogg' % (audio_link_start)
							if the_event8 == 'attack':
								the_result8 = '%shs/sounds/enus/VO_OG_133_Male_OldGod_Attack_01.ogg' % (audio_link_start)
							if the_event8 == 'death':
								the_result8 = '%s/hs/sounds/enus/VO_OG_133_Male_OldGod_Death_01.ogg' % (audio_link_start)
						elif the_card8 == 'N\'zoth, the Corruptor':
							if the_event8 == 'play':
								the_result8 = '%s/hs/sounds/enus/VO_OG_042_Male_OldGod_Play_01.ogg' % (audio_link_start)
							if the_event8 == 'attack':
								the_result8 = '%s/hs/sounds/enus/VO_OG_042_Male_OldGod_Attack_01.ogg' % (audio_link_start)
							if the_event8 == 'death':
								the_result8 = '%s/hs/sounds/enus/VO_OG_042_Male_OldGod_Death_01.ogg' % (audio_link_start)
						elif the_card8 == 'Nefarian':
							if the_event8 == 'death' or the_event8 == 'attack':
								the_result8 = SoundFinder(the_card_link8,the_event8)
							else:
								the_result8 = '%s%s' % (audio_link_start,the_event8)
						elif the_card8 == 'Rend Blackhand':
							if the_event8 == 'play':
								the_result8 = '%s/hs/sounds/enus/VO_BRMA09_1_START_01.ogg' % (audio_link_start)
							if the_event8 == 'attack':
								the_result8 = '%s/hs/sounds/enus/VO_BRMA09_1_RESPONSE_04.ogg' % (audio_link_start)
							if the_event8 == 'death':
								the_result8 = SoundFinder(the_card_link8,the_event8)
						elif the_card8 == 'Emperor Thaurissan':
							if the_event8 == 'play':
								the_result8 = '%s/hs/sounds/enus/VO_BRMA03_1_CARD_04.ogg' % (audio_link_start)
							if the_event8 == 'attack':
								the_result8 = '%s/hs/sounds/enus/VO_BRMA03_1_HERO_POWER_06.ogg' % (audio_link_start)
							if the_event8 == 'death':
								the_result8 = SoundFinder(the_card_link8,the_event8)
						elif the_card8 == 'Majordomo Executus':
							if the_event8 == 'play':
								the_result8 = '%s/hs/sounds/enus/VO_BRMA06_1_START_01.ogg' % (audio_link_start)
							if the_event8 == 'attack':
								the_result8 = '%s/hs/sounds/enus/VO_BRMA06_1_TURN1_02_ALT.ogg' % (audio_link_start)
							if the_event8 == 'death':
								the_result8 = SoundFinder(the_card_link8,the_event8)
					if the_result8 != None:
						the_reply8 = '''* %s\'s[%s](%s)
		
		
''' % (the_card8, event_caller8, the_result8)
						print the_reply8
				if the_card8 != '' and the_event8 != '' and hero_card8 == True:
					if the_result8 != None:
						the_reply8 = '''* %s\'s [%s line.](%s) 
		
		
''' % (the_card8, the_event8, the_result8)
					print the_reply8
				if the_card9 != '' and the_event9 != '' and hero_card9 == False:
					if the_card9 not in list_of_exceptions:
						the_result9 = SoundFinder(the_card_link9,the_event9)
					elif the_card9 in list_of_exceptions:
						if the_card9 == 'C\'thun':
							if the_event9 == 'trigger':
								dice_roll = randint(0,11)
								the_result9 = '%s%s' % (audio_link_start, cthun_triggers[dice_roll])
							for i in range(0,11):
								if the_event9 == cthun_triggers[i]:
									the_result9 = '%s%s' % (audio_link_start,the_event9)
								elif i == 11:
									the_result9 = SoundFinder(the_card_link9,the_event9)
						elif the_card9 == 'Y\'Shaarj, Rage Unbound':
							if the_event9 == 'play':
								the_result9 = '%s/hs/sounds/enus/VO_OG_133_Male_OldGod_Play_01.ogg' % (audio_link_start)
							if the_event9 == 'attack':
								the_result9 = '%shs/sounds/enus/VO_OG_133_Male_OldGod_Attack_01.ogg' % (audio_link_start)
							if the_event9 == 'death':
								the_result9 = '%s/hs/sounds/enus/VO_OG_133_Male_OldGod_Death_01.ogg' % (audio_link_start)
						elif the_card9 == 'N\'zoth, the Corruptor':
							if the_event9 == 'play':
								the_result9 = '%s/hs/sounds/enus/VO_OG_042_Male_OldGod_Play_01.ogg' % (audio_link_start)
							if the_event9 == 'attack':
								the_result9 = '%s/hs/sounds/enus/VO_OG_042_Male_OldGod_Attack_01.ogg' % (audio_link_start)
							if the_event9 == 'death':
								the_result9 = '%s/hs/sounds/enus/VO_OG_042_Male_OldGod_Death_01.ogg' % (audio_link_start)
						elif the_card9 == 'Nefarian':
							if the_event9 == 'death' or the_event9 == 'attack':
								the_result9 = SoundFinder(the_card_link9,the_event9)
							else:
								the_result9 = '%s%s' % (audio_link_start,the_event9)
						elif the_card9 == 'Rend Blackhand':
							if the_event9 == 'play':
								the_result9 = '%s/hs/sounds/enus/VO_BRMA09_1_START_01.ogg' % (audio_link_start)
							if the_event9 == 'attack':
								the_result9 = '%s/hs/sounds/enus/VO_BRMA09_1_RESPONSE_04.ogg' % (audio_link_start)
							if the_event9 == 'death':
								the_result9 = SoundFinder(the_card_link9,the_event9)
						elif the_card9 == 'Emperor Thaurissan':
							if the_event9 == 'play':
								the_result9 = '%s/hs/sounds/enus/VO_BRMA03_1_CARD_04.ogg' % (audio_link_start)
							if the_event9 == 'attack':
								the_result9 = '%s/hs/sounds/enus/VO_BRMA03_1_HERO_POWER_06.ogg' % (audio_link_start)
							if the_event9 == 'death':
								the_result9 = SoundFinder(the_card_link9,the_event9)
						elif the_card9 == 'Majordomo Executus':
							if the_event9 == 'play':
								the_result9 = '%s/hs/sounds/enus/VO_BRMA06_1_START_01.ogg' % (audio_link_start)
							if the_event9 == 'attack':
								the_result9 = '%s/hs/sounds/enus/VO_BRMA06_1_TURN1_02_ALT.ogg' % (audio_link_start)
							if the_event9 == 'death':
								the_result9 = SoundFinder(the_card_link9,the_event9)
					if the_result9 != None:
						the_reply9 = '''* %s\'s[%s](%s)
		
		
''' % (the_card9, event_caller9, the_result9)
						print the_reply9
				if the_card9 != '' and the_event9 != '' and hero_card9 == True:
					if the_result9 != None:
						the_reply9 = '''* %s\'s [%s line.](%s) 
		
		
''' % (the_card9, the_event9, the_result9)
					print the_reply9
				if the_card10 != '' and the_event10 != '' and hero_card10 == False:
					if the_card10 not in list_of_exceptions:
						the_result10 = SoundFinder(the_card_link10,the_event10)
					elif the_card10 in list_of_exceptions:
						if the_card10 == 'C\'thun':
							if the_event10 == 'trigger':
								dice_roll = randint(0,11)
								the_result10 = '%s%s' % (audio_link_start, cthun_triggers[dice_roll])
							for i in range(0,11):
								if the_event10 == cthun_triggers[i]:
									the_result10 = '%s%s' % (audio_link_start,the_event10)
								elif i == 11:
									the_result10 = SoundFinder(the_card_link10,the_event10)
						elif the_card10 == 'Y\'Shaarj, Rage Unbound':
							if the_event10 == 'play':
								the_result10 = '%s/hs/sounds/enus/VO_OG_133_Male_OldGod_Play_01.ogg' % (audio_link_start)
							if the_event10 == 'attack':
								the_result10 = '%shs/sounds/enus/VO_OG_133_Male_OldGod_Attack_01.ogg' % (audio_link_start)
							if the_event10 == 'death':
								the_result10 = '%s/hs/sounds/enus/VO_OG_133_Male_OldGod_Death_01.ogg' % (audio_link_start)
						elif the_card10 == 'N\'zoth, the Corruptor':
							if the_event10 == 'play':
								the_result10 = '%s/hs/sounds/enus/VO_OG_042_Male_OldGod_Play_01.ogg' % (audio_link_start)
							if the_event10 == 'attack':
								the_result10 = '%s/hs/sounds/enus/VO_OG_042_Male_OldGod_Attack_01.ogg' % (audio_link_start)
							if the_event10 == 'death':
								the_result10 = '%s/hs/sounds/enus/VO_OG_042_Male_OldGod_Death_01.ogg' % (audio_link_start)
						elif the_card10 == 'Nefarian':
							if the_event10 == 'death' or the_event10 == 'attack':
								the_result10 = SoundFinder(the_card_link10,the_event10)
							else:
								the_result10 = '%s%s' % (audio_link_start,the_event10)
						elif the_card10 == 'Rend Blackhand':
							if the_event10 == 'play':
								the_result10 = '%s/hs/sounds/enus/VO_BRMA09_1_START_01.ogg' % (audio_link_start)
							if the_event10 == 'attack':
								the_result10 = '%s/hs/sounds/enus/VO_BRMA09_1_RESPONSE_04.ogg' % (audio_link_start)
							if the_event10 == 'death':
								the_result10 = SoundFinder(the_card_link10,the_event10)
						elif the_card10 == 'Emperor Thaurissan':
							if the_event10 == 'play':
								the_result10 = '%s/hs/sounds/enus/VO_BRMA03_1_CARD_04.ogg' % (audio_link_start)
							if the_event10 == 'attack':
								the_result10 = '%s/hs/sounds/enus/VO_BRMA03_1_HERO_POWER_06.ogg' % (audio_link_start)
							if the_event10 == 'death':
								the_result10 = SoundFinder(the_card_link10,the_event10)
						elif the_card10 == 'Majordomo Executus':
							if the_event10 == 'play':
								the_result10 = '%s/hs/sounds/enus/VO_BRMA06_1_START_01.ogg' % (audio_link_start)
							if the_event10 == 'attack':
								the_result10 = '%s/hs/sounds/enus/VO_BRMA06_1_TURN1_02_ALT.ogg' % (audio_link_start)
							if the_event10 == 'death':
								the_result10 = SoundFinder(the_card_link10,the_event10)
					if the_result10 != None:
						the_reply10 = '''* %s\'s[%s](%s)
		
		
''' % (the_card10, event_caller10, the_result10)
						print the_reply10
				if the_card10 != '' and the_event10 != '' and hero_card10 == True:
					if the_result10 != None:
						the_reply10 = '''* %s\'s [%s line.](%s) 
		
		
''' % (the_card10, the_event10, the_result10)
					print the_reply10
				#These two if statments will reply a random precreated message to the common "good bot" and "bad bot" replies.  The if statment checks if a reply is one of the famous responses.
				#Then it will check the parent comment's author to check if the reply is aimed at the hearthsound_bot.
				#Then if it is, the bot will get a random number from randint and then choose a funny response to reply based off of the random number it gets.
				if text == 'good-bot':
					if comment.parent().author.name == os.environ.get('reddit_username'):
						dice_roll = randint(1,4)
						if dice_roll == 1:
							the_reply = '*Great bot'
						elif dice_roll == 2:
							the_reply = 'Shut up baby, I know it!'
						elif dice_roll == 3:
							the_reply = 'And I love you, random citizen!'
						elif dice_roll == 4:
							the_reply = 'The obvious conclusion.'
				if text == 'bad-bot':
					if comment.parent().author.name == os.environ.get('reddit_username'):
						dice_roll = randint(1,4)
						if dice_roll == 1:
							the_reply = 'Hearthsound_bot still not good bot?u punks are never satisfied are you?Hope you love being bitter because I definitely love being the greatest'
						elif dice_roll == 2:
							the_reply = 'rank 25 player'
						elif dice_roll == 3:
							the_reply = 'no u'
						elif dice_roll == 4:
							the_reply = 'This is outrageous, it\'s unfair!'
				if text == 'how-long-can-this-go-on?':
					try:
						if comment.parent().body == 'how-long-can-this-go-on?':
							the_reply = '[How long can this go on?](http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_ICC_466_Male_Draenei_Play_01.ogg)'
					except praw.exceptions.PRAWException as e:
						print 'this works'
						if e.error_type == 'AttributeError':
							print 'and so does this'
							cache.append(comment.id)
							if len(cache) == 101:
								cache.pop(0)
							pass
				#This is where the reply is created.  It checks out many replies are filled in by going from the last reply that would be filled in to the first reply.
				#When the amount of replies filled in is found, the program puts them all into a single reply called true_reply.  It then uses the PRAW reply command to send the reply off to Reddit. 
				if the_reply != '':
					true_reply = '%s%s%s%s%s%s%s%s%s%s' % (the_reply,the_reply2,the_reply3,the_reply4,the_reply5,the_reply6,the_reply7,the_reply8,the_reply9,the_reply10)
					comment.reply(true_reply)
				
		
				#Here, all of the variables that could've been used are reset to blank as to avoid previous replies messing up future ones.
				#The cache is a list of all comments that have been replied to.  Since Reddit stream only reads the 100 latest comments I remove the 101st comment in the cache to free up space.
				cache.append(comment.id)
				if len(cache) == 101:
					cache.pop(0)
				true_reply = ''
				the_card = ''
				the_event = ''
				the_reply = ''
				the_card2 = ''
				the_event2 = ''
				the_reply2 = ''
				the_card3 = ''
				the_event3 = ''
				the_reply3 = ''
				the_card4 = ''
				the_event4 = ''
				the_reply4 = ''
				the_card5 = ''
				the_event5 = ''
				the_reply5 = ''
				the_card6 = ''
				the_event6 = ''
				the_reply6 = ''
				the_card7 = ''
				the_event7 = ''
				the_reply7 = ''
				the_card8 = ''
				the_event8 = ''
				the_reply8 = ''
				the_card9 = ''
				the_event9 = ''
				the_reply9 = ''
				the_card10 = ''
				the_event10 = ''
				the_reply10 = ''
				the_result = None
				event_caller = None
				the_result2 = None
				event_caller2 = None
				the_result3 = None
				event_caller3 = None
				the_result4 = None
				event_caller4 = None
				the_result5 = None
				event_caller5 = None
				the_result6 = None
				event_caller6 = None
				the_result7 = None
				event_caller7 = None
				the_result8 = None
				event_caller8 = None
				the_result9 = None
				event_caller9 = None
				the_result10 = None
				event_caller10 = None
				hero_card = False
				hero_card2 = False
				hero_card3 = False
				hero_card4 = False
				hero_card5 = False
				hero_card6 = False
				hero_card7 = False
				hero_card8 = False
				hero_card9 = False
				hero_card10 = False
			except praw.exceptions.APIException as e:
				if e.error_type == 'RATELIMIT':
					try:
						error_time = re.search(r'[\d][\d]?',str(e))
						if error_time:
							time_error = '%s' % (error_time.group(0))
							time_error = int(time_error)
						error_mins = re.search(r'minute',str(e))
						if error_mins:
							time_error = time_error*60 + 60
						print e
						print 'waiting for %s seconds' % time_error
						time.sleep(time_error)
						print 'DONE SLEEPING'
						comment.reply(true_reply)
						cache.append(comment.id)
						if len(cache) == 101:
							cache.pop(0)
						true_reply = ''
						the_card = ''
						the_event = ''
						the_reply = ''
						the_card2 = ''
						the_event2 = ''
						the_reply2 = ''
						the_card3 = ''
						the_event3 = ''
						the_reply3 = ''
						the_card4 = ''
						the_event4 = ''
						the_reply4 = ''
						the_card5 = ''
						the_event5 = ''
						the_reply5 = ''
						the_card6 = ''
						the_event6 = ''
						the_reply6 = ''
						the_card7 = ''
						the_event7 = ''
						the_reply7 = ''
						the_card8 = ''
						the_event8 = ''
						the_reply8 = ''
						the_card9 = ''
						the_event9 = ''
						the_reply9 = ''
						the_card10 = ''
						the_event10 = ''
						the_reply10 = ''
						the_result = None
						event_caller = None
						the_result2 = None
						event_caller2 = None
						the_result3 = None
						event_caller3 = None
						the_result4 = None
						event_caller4 = None
						the_result5 = None
						event_caller5 = None
						the_result6 = None
						event_caller6 = None
						the_result7 = None
						event_caller7 = None
						the_result8 = None
						event_caller8 = None
						the_result9 = None
						event_caller9 = None
						the_result10 = None
						event_caller10 = None
						comment_list = []
						hero_card = False
						hero_card2 = False
						hero_card3 = False
						hero_card4 = False
						hero_card5 = False
						hero_card6 = False
						hero_card7 = False
						hero_card8 = False
						hero_card9 = False
						hero_card10 = False
						
						continue
					except praw.exceptions.APIException as e:
						if e.error_type == 'DELETED_COMMENT':
							print "deleted comment error."
							true_reply = ''
							the_card = ''
							the_event = ''
							the_reply = ''
							the_card2 = ''
							the_event2 = ''
							the_reply2 = ''
							the_card3 = ''
							the_event3 = ''
							the_reply3 = ''
							the_card4 = ''
							the_event4 = ''
							the_reply4 = ''
							the_card5 = ''
							the_event5 = ''
							the_reply5 = ''
							the_card6 = ''
							the_event6 = ''
							the_reply6 = ''
							the_card7 = ''
							the_event7 = ''
							the_reply7 = ''
							the_card8 = ''
							the_event8 = ''
							the_reply8 = ''
							the_card9 = ''
							the_event9 = ''
							the_reply9 = ''
							the_card10 = ''
							the_event10 = ''
							the_reply10 = ''
							the_result = None
							event_caller = None
							the_result2 = None
							event_caller2 = None
							the_result3 = None
							event_caller3 = None
							the_result4 = None
							event_caller4 = None
							the_result5 = None
							event_caller5 = None
							the_result6 = None
							event_caller6 = None
							the_result7 = None
							event_caller7 = None
							the_result8 = None
							event_caller8 = None
							the_result9 = None
							event_caller9 = None
							the_result10 = None
							event_caller10 = None
							comment_list = []
							hero_card = False
							hero_card2 = False
							hero_card3 = False
							hero_card4 = False
							hero_card5 = False
							hero_card6 = False
							hero_card7 = False
							hero_card8 = False
							hero_card9 = False
							hero_card10 = False
							break
				if e.error_type == 'DELETED_COMMENT':
					print "deleted comment error."
					true_reply = ''
					the_card = ''
					the_event = ''
					the_reply = ''
					the_card2 = ''
					the_event2 = ''
					the_reply2 = ''
					the_card3 = ''
					the_event3 = ''
					the_reply3 = ''
					the_card4 = ''
					the_event4 = ''
					the_reply4 = ''
					the_card5 = ''
					the_event5 = ''
					the_reply5 = ''
					the_card6 = ''
					the_event6 = ''
					the_reply6 = ''
					the_card7 = ''
					the_event7 = ''
					the_reply7 = ''
					the_card8 = ''
					the_event8 = ''
					the_reply8 = ''
					the_card9 = ''
					the_event9 = ''
					the_reply9 = ''
					the_card10 = ''
					the_event10 = ''
					the_reply10 = ''
					the_result = None
					event_caller = None
					the_result2 = None
					event_caller2 = None
					the_result3 = None
					event_caller3 = None
					the_result4 = None
					event_caller4 = None
					the_result5 = None
					event_caller5 = None
					the_result6 = None
					event_caller6 = None
					the_result7 = None
					event_caller7 = None
					the_result8 = None
					event_caller8 = None
					the_result9 = None
					event_caller9 = None
					the_result10 = None
					event_caller10 = None
					comment_list = []
					hero_card = False
					hero_card2 = False
					hero_card3 = False
					hero_card4 = False
					hero_card5 = False
					hero_card6 = False
					hero_card7 = False
					hero_card8 = False
					hero_card9 = False
					hero_card10 = False
					break
			comment_list = []
			break