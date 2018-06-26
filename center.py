# -*- coding: utf-8 -*-
from sound_finder import SoundFinder
from string import capwords
import praw
import secret
import re
from random import randint
import time
#SoundFinder (my own creation) is imported to get the links to the sounds from hearthhead.  capwords is imported from string to capitalize each word of a card name).
#praw is a module made specifically to help people make their own reddit bots... which I am using to make my own reddit bot.  secret holds information for praw which I don't want to pubically share.
#re is imported to better search for cards in comments and randint is imported to create a random number for later.

#This is the suggested setup for praw.  It takes the various ids hidden in secret to log the bot into reddit.
#Then it will use .stream to put the last 100 comments written in a certain subreddit like r/hearthstone into a list.
reddit = praw.Reddit(client_id=secret.client_id, client_secret = secret.secret_id, user_agent = secret.user_agent, username = secret.username, password = secret.password)
subreddit = reddit.subreddit('test')
comments = subreddit.stream.comments()


#While most of the card sounds will have to be called by stating the card and type of sound, I plan to have a few famous sounds be called a bit eaiser.  Like the priest wow.
wow = "http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_09_WOW_06.ogg"

special_lines = {'wow':'"http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_09_WOW_06.ogg"',}


#If a card is a boss in the game, they will have two different links on the hearthhead website.  So this is a dictonary of any cards with a differnt link from their name.
dic_of_multiples = {'kelthuzad': 'kelthuzad-1', 'cthun': 'cthun-1', 'emperor-thaurissan': 'emperor-thaurissan-2', 'majordomo-executus': 'majordomo-executus-2', 'rend-blackhand': 'rend-blackhand-2',
'chromaggus': 'chromaggus-2', 'nefarian': 'nefarian-7', 'blood-queen-lanathel': 'blood-queen-lanathel-2', 'professor-putricide': 'professor-putricide-1', 'sindragosa': 'sindragosa-4',
'the-darkness': 'the-darkness-2', 'prince-malchezaar': 'prince-malchezaar-4'}


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
'tolvir-warden': 'Tol\'vir warden', 'voljin': 'Vol\'jin', 'anubar-ambusher': "Anub'ar Ambusher", 'cthuns-chosen': 'C\'Thun\'s Chosen', 'faldorei-strider': 'Fal\'dorei Strider',
'arcane-nullifier-x-21': 'Arcane Nullifier X-21', 'bright-eyed-scout': 'Bright-Eyed Scout', 'enhance-o-mechano': 'Enhance-o Mechano', 'genzo-the-shark': 'Genzo, the Shark',
'korkron-elite': 'Kor\'kron Elite', 'mogushan-warden': 'Mogu\'shan Warden', 'senjin-shieldmasta': 'Sen\'jin Shieldmasta', 'sherazin-corpse-flower': 'Sherazin, Corpse Flower',
'gorillabot-a-3': 'Gorillabot A-3', 'klaxxi-amber-weaver': 'Klaxxi Amber-Weaver', 'mini-mage': 'Mini-Mage', 'old-murk-eye': 'Old Murk-Eye', 'tolvir-stoneshaper': 'Tol\'vir Stoneshaper',
'amgam-rager': 'Am\'gam Rager', 'disciple-of-cthun': 'Disciple of C\'thun', 'xaril-poisoned-mind': 'Xaril, Poisoned Mind', 'alarm-o-bot': 'Alarm-O-Bot', 'lights-champion': 'Light\'s Champion',
'lil-exorcist': 'Lil\' Exorcist', 'spawn-of-nzoth': 'Spawn of N\'zoth', 'hench-clan-thug': 'Hench-Clan Thug', 'shaku-the-collector': 'Shaku, the Collector', 'valkyr-soulclaimer': 'Val\'kyr Voulclaimer',
'witchs-cauldron': 'Witch\'s Cauldron', 'alexstraszas-champion': 'Alexstrasza\'s Champion', 'captains-parrot': 'Captain\'s Parrot', 'annoy-o-tron': 'Annoy-o-Tron',
'nat-the-darkfisher': 'Nat, the Darkfisher', 'kings-elekk': 'King\'s Elekk', 'medivhs-valet': 'Medivh\'s Valet', 'nerubar-weblord': 'Nerub\'ar Weblord', 'sorcerers-apprentice': 'Sorcerer\'s Apprentice',
'ships-cannon': 'Ship\'s Cannon', 'goblin-auto-barber': 'Goblin Auto-Barber', 'one-eyed-cheat': 'One-Eyed Cheat', 'pint-sized-summoner': 'Pint-Sized Summoner', 'scorp-o-matic': 'Scorp-o-matic',
'whirling-zap-o-matic': 'Whirling Zap-o-matic', 'small-time-buccaneer': 'Small-Time Buccaneer', 'malchezaars-imp': 'NMlchezaar\'s Imp', 'nzoths-first-mate': 'N\'zoth\'s First Mate',
'tentacle-of-nzoth': 'Tentacle of N\'zoth', 'witchs-apprentice': 'Witch\'s Appretice'}

#This is a list of all the minions currently in Hearthstone at the time of Witchwood.  It was made in card_list but copied into center so that the program doesn't have to remake the list each run.

minion_list = ['molten-giant', 'arcane-giant', 'clockwork-giant', 'mountain-giant', 'snowfury-giant', 'cthun', 'deathwing', 'deathwing-dragonlord', 'emeriss', 'faceless-behemoth', 'frost-giant', 'kun-the-forgotten-king', 'nzoth-the-corruptor', 'sea-giant', 'tyrantus', 'ultrasaur', 'varian-wrynn', 'yogg-saron-hopes-end', 'yshaarj-rage-unbound', 'alexstrasza', 'anubarak', 'arch-thief-rafaam', 'aviana', 'baku-the-mooneater', 'blade-of-cthun', 'blood-of-the-ancient-one', 'cenarius', 'dragoncaller-alanna', 'dragonhatcher', 'giant-mastodon', 'hadronox', 'icehowl', 'king-krush', 'king-mosh', 'krul-the-unshackled', 'lord-jaraxxus', 'majordomo-executus', 'malganis', 'malygos', 'master-oakheart', 'mayor-noggenfogger', 'mekgineer-thermaplugg', 'nefarian', 'north-sea-kraken', 'nozdormu', 'obsidian-statue', 'onyxia', 'ozruk', 'shudderwock', 'sleepy-dragon', 'soggoth-the-slitherer', 'voidlord', 'volcanic-lumberer', 'ysera', 'alakir-the-windlord', 'anomalus', 'bonemare', 'cauldron-elemental', 'charged-devilsaur', 'chromaggus', 'deranged-doctor', 'doomcaller', 'eldritch-horror', 'foe-reaper-4000', 'force-tank-max', 'fossilized-devilsaur', 'geosculptor-yip', 'giant-sand-worm', 'gilnean-royal-guard', 'grand-archivist', 'grizzled-guardian', 'grommash-hellscream', 'gruul', 'ironbark-protector', 'kalimos-primal-lord', 'kathrena-winterwisp', 'kelthuzad', 'king-togwaggle', 'marin-the-fox', 'medivh-the-guardian', 'naga-sea-witch', 'primordial-drake', 'ragnaros-the-firelord', 'ragnaros-lightlord', 'rhonin', 'rotface', 'sindragosa', 'sneeds-old-shredder', 'splintergraft', 'splitting-festeroot', 'tess-greymane', 'the-boogeymonster', 'the-lich-king', 'tirion-fordring', 'tortollan-primalist', 'violet-wurm', 'abominable-bowman', 'abyssal-enforcer', 'acidmaw', 'ancient-of-lore', 'ancient-of-war', 'ancient-shieldbearer', 'archbishop-benedictus', 'archmage-antonidas', 'azalina-soulthief', 'baron-geddon', 'blackhowl-gunspire', 'blazecaller', 'bog-creeper', 'bogshaper', 'captured-jormungar', 'chillmaw', 'chogall', 'confessor-paletress', 'core-hound', 'corridor-creeper', 'countess-ashmore', 'darkmire-moonkin', 'don-hancho', 'dr-boom', 'eadric-the-pure', 'fearsome-doomguard', 'flame-leviathan', 'furious-ettin', 'gahzrilla', 'giant-anaconda', 'grimestreet-protector', 'grotesque-dragonhawk', 'guardian-of-kings', 'hogger-doom-of-elwynn', 'inkmaster-solia', 'jade-chieftain', 'knight-of-the-wild', 'lord-godfrey', 'lynessa-sunsorrow', 'malkorok', 'malorne', 'neptulon', 'nightscale-matriarch', 'obsidian-destroyer', 'prophet-velen', 'ravenholdt-assassin', 'rend-blackhand', 'sated-threshadon', 'silver-vanguard', 'skycapn-kragg', 'spiteful-summoner', 'stone-sentinel', 'stormwatcher', 'stormwind-champion', 'swamp-king-dred', 'tar-lord', 'temporus', 'the-curator', 'troggzor-the-earthinator', 'twin-emperor-veklor', 'volcanosaur', 'war-golem', 'worgen-abomination', 'wyrmguard', 'ancient-harbinger', 'ancient-of-blossoms', 'anima-golem', 'archmage', 'argent-commander', 'aya-blackpaw', 'big-time-racketeer', 'blackguard', 'bolf-ramshield', 'bone-drake', 'book-wyrm', 'boulderfist-ogre', 'cabal-shadow-priest', 'cairne-bloodhoof', 'coffin-crasher', 'coldarra-drake', 'corrupted-seer', 'cruel-dinomancer', 'crystal-lion', 'cursed-castaway', 'dark-arakkoa', 'defias-cleaner', 'drakonid-crusher', 'dread-infernal', 'emperor-thaurissan', 'faceless-summoner', 'fight-promoter', 'fire-elemental', 'frost-elemental', 'frozen-crusher', 'furnacefire-colossus', 'gadgetzan-auctioneer', 'gazlowe', 'gelbin-mekkatorque', 'gemstudded-golem', 'genn-greymane', 'glinda-crowskin', 'grand-crusader', 'grumble-worldshaker', 'hemet-jungle-hunter', 'herald-volazj', 'hogger', 'hungry-ettin', 'illidan-stormrage', 'iron-juggernaut', 'ivory-knight', 'jade-behemoth', 'justicar-trueheart', 'kabal-crystal-runner', 'kabal-trafficker', 'kidnapper', 'kodorider', 'lady-in-white', 'leatherclad-hogleader', 'lord-of-the-arena', 'luckydo-buccaneer', 'madam-goya', 'maexxna', 'master-jouster', 'mech-bear-cat', 'menagerie-warden', 'moat-lurker', 'mogor-the-ogre', 'mogors-champion', 'moorabi', 'mossy-horror', 'mukla-tyrant-of-the-vale', 'mysterious-challenger', 'necrotic-geist', 'nerubian-prophet', 'nerubian-unraveler', 'ornery-direhorn', 'piloted-sky-golem', 'possessed-lackey', 'priestess-of-elune', 'reckless-rocketeer', 'reno-jackson', 'rin-the-first-disciple', 'sabretooth-stalker', 'savannah-highmane', 'scaled-nightmare', 'sea-reaver', 'seeping-oozeling', 'shieldmaiden', 'sideshow-spelleater', 'skeram-cultist', 'skulking-geist', 'spectral-pillager', 'spellweaver', 'sunkeeper-tarim', 'sunwalker', 'sylvanas-windrunner', 'temple-enforcer', 'the-beast', 'the-black-knight', 'the-mistcaller', 'the-skeleton-knight', 'thing-from-below', 'toki-time-tinker', 'toshley', 'trade-prince-gallywix', 'void-crusher', 'volcanic-drake', 'wilfred-fizzlebang', 'windfury-harpy', 'wind-up-burglebot', 'wobbling-runts', 'wrathion', 'abomination', 'alley-armorsmith', 'antique-healbot', 'anubisath-sentinel', 'arcane-tyrant', 'avian-watcher', 'azure-drake', 'bewitched-guardian', 'big-game-hunter', 'bittertide-hydra', 'blackwing-corruptor', 'blingtron-3000', 'blood-queen-lanathel', 'bloodworm', 'bolvar-fordragon', 'bolvar-fireblood', 'bomb-lobber', 'bomb-squad', 'bone-baron', 'bonfire-elemental', 'booty-bay-bodyguard', 'burgly-bully', 'captain-greenskin', 'carnivorous-cube', 'carrion-drake', 'chief-inspector', 'clockwork-automaton', 'clockwork-knight', 'cobalt-guardian', 'cobalt-scalebane',
'corpse-raiser', 'corpse-widow', 'corrosive-sludge', 'corrupted-healbot', 'crazed-worshipper', 'cryomancer', 'cult-apothecary', 'curio-collector', 'darius-crowley', 'dark-iron-skulker', 'darkscale-healer', 'darkshire-alchemist', 'darkspeaker', 'death-revenant', 'deathweb-spider', 'despicable-dreadlord', 'direhorn-hatchling', 'djinni-of-zephyrs', 'dollmaster-dorian', 'doomguard', 'doppelgangster', 'dragon-consort', 'drakonid-operative', 'druid-of-the-claw', 'druid-of-the-fang', 'duskfallen-aviana', 'earth-elemental', 'elise-the-trailblazer', 'elite-tauren-chieftain', 'ethereal-conjurer', 'ethereal-peddler', 'faceless-manipulator', 'fatespinner', 'fel-reaver', 'fen-creeper', 'festeroot-hulk', 'feugen', 'finja-the-flying-star', 'floating-watcher', 'frostwolf-warlord', 'fungalmancer', 'furbolg-mossbinder', 'ghostly-charger', 'glitter-moth', 'gloom-stag', 'green-jelly', 'grim-patron', 'grimestreet-enforcer', 'grook-fu-master', 'guild-recruiter', 'gurubashi-berserker', 'hallazeal-the-ascended', 'harrison-jones', 'hemet-nesingwary', 'ixlid-fungal-lord', 'junkbot', 'kabal-songstealer', 'king-of-beasts', 'knuckles', 'kvaldir-raider', 'leeroy-jenkins', 'loatheb', 'lotus-agents', 'lotus-assassin', 'lyra-the-sunshard', 'madder-bomber', 'menagerie-magician', 'mimirons-head', 'muck-hunter', 'muklas-champion', 'nesting-roc', 'nexus-champion-saraad', 'nightblade', 'ogre-ninja', 'onyx-bishop', 'pit-fighter', 'prince-liam', 'prince-malchezaar', 'princess-huhuran', 'psych-o-tron', 'quartermaster', 'quartz-elemental', 'ram-wrangler', 'raza-the-chained', 'recruiter', 'red-mana-wyrm', 'rotten-applebaum', 'salty-dog', 'second-rate-bruiser', 'servant-of-kalimos', 'servant-of-yogg-saron', 'shado-pan-rider', 'shadowcaster', 'siege-engine', 'silver-hand-knight', 'skelemancer', 'sludge-belcher', 'spectral-knight', 'spiked-hogrider', 'spiteful-smith', 'stalagg', 'stampeding-kodo', 'starving-buzzard', 'stormpike-commando', 'stranglethorn-tiger', 'streetwise-investigator', 'summoning-stone', 'sunborne-valkyr', 'tar-lurker', 'thunder-bluff-valiant', 'tolvir-warden', 'tomb-lurker', 'trogg-gloomeater', 'tundra-rhino', 'tuskarr-jouster', 'twilight-darkmender', 'upgraded-repair-bot', 'usher-of-souls', 'validated-doomsayer', 'venomancer', 'venture-co-mercenary', 'verdant-longneck', 'vilebrood-skitterer', 'vilespine-slayer', 'virmen-sensei', 'voljin', 'voodoo-hexxer', 'white-eyes', 'windshear-stormcaller', 'witchwood-grizzly', 'aberrant-berserker', 'ancient-brewmaster', 'ancient-mage', 'ancient-shade', 'animated-armor', 'anubar-ambusher', 'arathi-weaponsmith', 'arcane-keysmith', 'arcane-nullifier-x-21', 'arcanosmith', 'arfus', 'armored-warhorse', 'arrogant-crusader', 'astral-tiger', 'auchenai-soulpriest', 'axe-flinger', 'backroom-bouncer', 'barnes', 'baron-rivendare', 'bellringer-sentry', 'blackwater-pirate', 'blood-witch', 'bloodhoof-brave', 'bright-eyed-scout', 'burly-rockjaw-trogg', 'chillblade-champion', 'chillwind-yeti', 'core-rager', 'corpsetaker', 'crowd-favorite', 'crystalweaver', 'cthuns-chosen', 'cult-master', 'cursed-disciple', 'cyclopian-horror', 'dalaran-aspirant', 'daring-reporter', 'dark-iron-dwarf', 'deathaxe-punisher', 'defender-of-argus', 'demented-frostcaller', 'dispatch-kodo', 'draenei-totemcarver', 'dragonkin-sorcerer', 'dragonling-mechanic', 'dread-corsair', 'dreadsteed', 'dunemaul-shaman', 'duskbreaker', 'eater-of-secrets', 'ebon-dragonsmith', 'eerie-statue', 'elise-starseeker', 'elven-minstrel', 'enhance-o-mechano', 'ethereal-arcanist', 'evil-heckler', 'evolved-kobold', 'exploding-bloatbat', 'faceless-shambler', 'faldorei-strider', 'fandral-staghelm', 'fel-cannon', 'felsoul-inquisitor', 'fire-plume-phoenix', 'fireguard-destroyer', 'flamewreathed-faceless', 'forest-guide', 'frigid-snobold', 'gentle-megasaur', 'genzo-the-shark', 'ghastly-conjurer', 'gnomish-inventor', 'goblin-blastmage', 'gorillabot-a-3', 'gormok-the-impaler', 'grave-shambler', 'grim-necromancer', 'grimy-gadgeteer', 'hoarding-dragon', 'holy-champion', 'hooded-acolyte', 'hooked-reaver', 'houndmaster', 'houndmaster-shaw', 'hozen-healer', 'hungry-dragon', 'infested-tauren', 'infested-wolf', 'ironwood-golem', 'jade-spirit', 'jeeves', 'jinyu-waterspeaker', 'jungle-moonkin', 'kabal-chemist', 'kazakus', 'keening-banshee', 'keeper-of-the-grove', 'keeper-of-uldaman', 'kezan-mystic', 'klaxxi-amber-weaver', 'kobold-illusionist', 'kobold-monk', 'kooky-chemist', 'korkron-elite', 'lakkari-felhound', 'leyline-manipulator', 'lifedrinker', 'lightfused-stegodon', 'lightspawn', 'lilian-voss', 'lost-tallstrider', 'lotus-illusionist', 'mad-hatter', 'magnataur-alpha', 'maiden-of-the-lake', 'master-of-disguise', 'master-of-evolution', 'meat-wagon', 'mechanical-yeti', 'midnight-drake', 'militia-commander', 'mini-mage', 'mire-keeper', 'mistwraith', 'mogushan-warden', 'murloc-knight', 'naga-corsair', 'night-howler', 'night-prowler', 'oasis-snapjaw', 'ogre-magi', 'old-murk-eye', 'phantom-freebooter', 'piloted-shredder', 'pit-lord', 'polluted-hoarder', 'priest-of-the-feast', 'prince-valanar', 'professor-putricide', 'rattling-rascal', 'ravenous-pterrordax', 'refreshment-vendor', 'rumbling-elemental', 'runeforge-haunter', 'sandbinder', 'saronite-chain-gang', 'savage-combatant', 'scaleworm', 'screwjank-clunker', 'seadevil-stinger', 'senjin-shieldmasta', 'shadow-sensei', 'shellshifter', 'sherazin-corpse-flower', 'shifting-shade', 'shimmering-courser', 'shroom-brewer', 'siltfin-spiritwalker', 'silvermoon-guardian', 'sneaky-devil', 'southsea-squidface', 'spawn-of-shadows', 'spellbreaker', 'spiritsinger-umbra', 'steam-surger', 'stegodon', 'stormwind-knight', 'strongshell-scavenger', 'summoning-portal', 'swift-messenger', 'tanaris-hogchopper', 'the-darkness', 'the-glass-knight', 'the-voraxx', 'ticking-abomination', 'tolvir-stoneshaper', 'tomb-pillager', 'tomb-spider', 'tortollan-shellraiser', 'totem-cruncher', 'tournament-medic', 'toxmonger', 'twilight-drake', 'twilight-guardian', 'twilight-summoner', 'unpowered-steambot', 'vex-crow', 'violet-teacher', 'voidcaller', 'wailing-soul', 'water-elemental', 'wee-spellstopper', 'wicked-skeleton', 'wicked-witchdoctor', 'wildwalker', 'windspeaker', 'witchwood-piper', 'worgen-greaser', 'xaril-poisoned-mind', 'acolyte-of-agony', 'acolyte-of-pain', 'addled-grizzly', 'alarm-o-bot', 'aldor-peacekeeper', 'amgam-rager', 'arcane-golem', 'argent-horserider', 'auctionmaster-beardo', 'backstreet-leper', 'bearshark', 'benevolent-djinn', 'black-cat', 'blackwald-pixie', 'blackwing-technician', 'blink-fox', 'blood-knight', 'bloodsail-cultist', 'blubber-baron', 'boisterous-bard', 'brann-bronzebeard', 'carrion-grub', 'cave-hydra', 'celestial-dreamer', 'chittering-tunneler', 'cloaked-huntress', 'coldlight-oracle', 'coldlight-seer', 'coldwraith', 'coliseum-manager', 'crypt-lord', 'curious-glimmerroot', 'cutthroat-buccaneer', 'dalaran-mage', 'dancing-swords', 'dark-cultist', 'darkshire-councilman', 'deadly-fork', 'deathlord', 'deathspeaker', 'demolisher', 'desert-camel', 'devilsaur-egg', 'disciple-of-cthun', 'doomed-apprentice', 'dragonhawk-rider', 'dragonslayer', 'drakkari-defender', 'drakkari-enchanter', 'dreadscale', 'druid-of-the-flame', 'druid-of-the-scythe', 'duskbat', 'duskhaven-hunter', 'earthen-ring-farseer', 'edwin-vancleef', 'eggnapper', 'elder-longneck', 'emperor-cobra', 'eydis-darkbane', 'face-collector', 'fel-orc-soulfiend', 'felguard', 'fencing-coach', 'fierce-monkey', 'fjola-lightbane', 'flamewaker', 'flesheating-ghoul', 'flying-machine', 'forlorn-stalker', 'frothing-berserker', 'fungal-enchanter', 'giant-wasp', 'gilded-gargoyle', 'gluttonous-ooze', 'gnomeregan-infantry', 'gnomish-experimenter', 'goblin-sapper', 'greedy-sprite', 'grimestreet-pawnbroker', 'grimestreet-smuggler', 'grove-tender', 'happy-ghoul', 'harvest-golem', 'hench-clan-thug', 'hired-gun', 'hobgoblin', 'hot-spring-guardian', 'howlfiend', 'howling-commander', 'humongous-razorleaf', 'hyldnir-frostrider', 'ice-rager', 'igneous-elemental', 'illuminator', 'imp-gang-boss', 'imp-master', 'injured-blademaster', 'iron-sensei', 'ironbeak-owl', 'ironforge-rifleman', 'ironfur-grizzly', 'jungle-panther', 'kabal-courier', 'kabal-talonpriest', 'king-mukla', 'kirin-tor-mage', 'kobold-apprentice', 'kobold-barbarian', 'lights-champion', 'lil-exorcist', 'lone-champion', 'magma-rager', 'mana-tide-totem', 'manic-soulcaster', 'marsh-drake', 'master-of-ceremonies', 'metaltooth-leaper', 'mind-control-tech', 'mindbreaker', 'mirage-caller', 'moroes', 'mountainfire-armor', 'mounted-raptor', 'murloc-warleader', 'nightbane-templar', 'nightmare-amalgam', 'ogre-brute', 'orgrimmar-aspirant', 'pantry-spider', 'paragon-of-light', 'phantom-militia', 'plague-scientist', 'primalfin-lookout', 'prince-taldaram', 'pterrordax-hatchling', 'pumpkin-peasant', 'questing-adventurer', 'rabid-worgen', 'raging-worgen', 'raid-leader', 'rat-pack', 'ratcatcher', 'ravaging-ghoul', 'ravencaller', 'razorfen-hunter', 'rummaging-kobold', 'saboteur', 'scarlet-crusader', 'scarlet-purifier', 'sergeant-sally', 'sewer-crawler', 'shade-of-naxxramas', 'shadow-rager', 'shadowfiend', 'shady-dealer', 'shaku-the-collector', 'shaky-zipgunner', 'shallow-gravedigger', 'shattered-sun-cleric', 'shrieking-shroom', 'si-7-agent', 'silent-knight', 'silithid-swarmer', 'silver-hand-regent', 'silverback-patriarch', 'silverware-golem', 'sonya-shadowdancer', 'soot-spewer', 'southsea-captain', 'spawn-of-nzoth', 'spellslinger', 'spider-tank', 'squirming-tentacle', 'stablemaster', 'steward-of-darkshire', 'stitched-tracker', 'stonehill-defender', 'stoneskin-basilisk', 'stoneskin-gargoyle', 'street-trickster', 'tanglefur-mystic', 'tar-creeper', 'tauren-warrior', 'terrorscale-stalker', 'thrallmar-farseer', 'thunder-lizard', 'tinkertown-technician', 'tinkmaster-overspark', 'toothy-chest', 'toxic-sewer-ooze', 'tuskarr-totemic', 'twilight-acolyte', 'twilight-elder', 'twilight-flamecaller', 'unbound-elemental', 'unearthed-raptor', 'unlicensed-apothecary', 'valkyr-soulclaimer', 'vicious-fledgling', 'violet-illusionist', 'void-ripper', 'void-terror', 'voodoo-doll', 'vryghoul', 'walnut-sprite', 'warhorse-trainer', 'warsong-commander', 'wickerflame-burnbristle', 'witchs-cauldron', 'wolfrider', 'zola-the-gorgon', 'zoobot', 'acidic-swamp-ooze', 'alexstraszas-champion', 'amani-berserker', 'ancient-watcher', 'annoy-o-tron', 'anodized-robo-cub', 'arcanologist', 'archmage-arugal', 'argent-protector', 'argent-watchman', 'armorsmith', 'baleful-banker', 'beckoner-of-evil', 'bilefin-tidehunter', 'biteweed', 'bloodfen-raptor', 'bloodmage-thalnos', 'bloodsail-raider', 'blowgill-sniper', 'bluegill-warrior', 'boneguard-lieutenant', 'brrrloc', 'captains-parrot', 'cathedral-gargoyle', 'cavern-shinyfinder', 'clutchmother-zavas', 'cornered-sentry', 'crackling-razormaw', 'crazed-alchemist', 'cruel-taskmaster', 'cult-sorcerer', 'cutpurse', 'dark-peddler', 'darkshire-librarian', 'darnassus-aspirant', 'defias-ringleader', 'dire-wolf-alpha', 'dirty-rat', 'doomsayer', 'druid-of-the-saber', 'druid-of-the-swarm', 'drygulch-jailor', 'drywhisker-armorer', 'duskboar', 'echoing-ooze', 'eternal-sentinel', 'explosive-sheep', 'faerie-dragon', 'fallen-hero', 'fallen-sun-cleric', 'fire-plume-harbinger', 'flame-juggler', 'flametongue-totem', 'friendly-bartender', 'frostwolf-grunt', 'gadgetzan-ferryman', 'gadgetzan-socialite', 'garrison-commander', 'ghost-light-angler', 'gilblin-stalker', 'gnomeferatu', 'goblin-auto-barber', 'golakka-crawler', 'grimestreet-informant', 'grimestreet-outfitter', 'haunted-creeper', 'hobart-grapplehammer', 'huge-toad', 'hunting-mastiff', 'hydrologist', 'ice-walker', 'jade-swarmer', 'jeweled-scarab', 'kindly-grandmother', 'kings-elekk', 'knife-juggler', 'kobold-geomancer', 'kobold-hermit', 'lance-carrier', 'lightwell', 'loot-hoarder', 'lorewalker-cho', 'lost-spirit', 'mad-bomber', 'mad-scientist', 'mana-addict', 'mana-geode', 'mana-wraith', 'master-swordsmith', 'mechwarper', 'medivhs-valet', 'micro-machine', 'millhouse-manastorm', 'mistress-of-pain', 'murkspark-eel', 'murloc-tidehunter', 'murmuring-elemental', 'museum-curator', 'nat-pagle', 'nat-the-darkfisher', 'nerubar-weblord', 'nerubian-egg', 'netherspite-historian', 'novice-engineer', 'one-eyed-cheat', 'patient-assassin', 'pint-sized-summoner', 'plated-beetle', 'pompous-thespian', 'primalfin-champion', 'primalfin-totem', 'prince-keleseth', 'public-defender', 'puddlestomper', 'pyros', 'radiant-elemental', 'ravasaur-runt', 'raven-familiar', 'razorpetal-lasher', 'recombobulator', 'redband-wasp', 'river-crocolisk', 'rockpool-hunter', 'scavenging-hyena', 'scorp-o-matic', 'shadow-ascendant', 'shadowboxer', 'shielded-minibot', 'shimmering-tempest', 'ships-cannon', 'shrinkmeister', 'snowchugger', 'sorcerers-apprentice', 'sparring-partner', 'spellshifter', 'squashling', 'steamwheedle-sniper', 'stonesplinter-trogg', 'stubborn-gastropod', 'succubus', 'sunfury-protector', 'tainted-zealot', 'tiny-knight-of-evil', 'tortollan-forager', 'totem-golem', 'trogg-beastrager', 'tuskarr-fisherman', 'twilight-geomancer', 'twisted-worgen', 'undercity-huckster', 'undercity-valiant', 'unstable-ghoul', 'vicious-scalehide', 'vitality-totem', 'volatile-elemental', 'vulgar-homunculus', 'whirling-zap-o-matic', 'wild-pyromancer', 'wrathguard', 'wyrmrest-agent', 'youthful-brewmaster', 'abusive-sergeant', 'acherus-veteran', 'air-elemental', 'alleycat', 'angry-chicken', 'animated-berserker', 'arcane-anomaly', 'arcane-artificer', 'argent-squire', 'babbling-book', 'bladed-cultist', 'blood-imp', 'bloodsail-corsair', 'brave-archer', 'buccaneer', 'chameleos', 'clockwork-gnome', 'cogmaster', 'crystalline-oracle', 'deadscale-knight', 'dire-mole', 'dragon-egg', 'dust-devil', 'elven-archer', 'emerald-hive-queen', 'emerald-reaver', 'enchanted-raven', 'feral-gibberer', 'fiery-bat', 'fire-fly', 'flame-imp', 'forbidden-ancient', 'gadgetzan-jouster', 'glacial-shard', 'goldshire-footman', 'gravelsnout-knight', 'grimscale-chum', 'grimscale-oracle', 'hungry-crab', 'injured-kvaldir', 'jeweled-macaw', 'kabal-lackey', 'kobold-librarian', 'leper-gnome', 'lightwarden', 'lowly-squire', 'malchezaars-imp', 'mana-wyrm', 'meanstreet-marshal', 'mistress-of-mixtures', 'murloc-raider', 'murloc-tidecaller', 'northshire-cleric', 'nzoths-first-mate', 'patches-the-pirate', 'pit-snake', 'possessed-villager', 'raptor-hatchling', 'reliquary-seeker', 'righteous-protector', 'runic-egg', 'sanguine-reveler', 'secretkeeper', 'selfless-hero', 'shadowbomber', 'shieldbearer', 'shifter-zerus', 'sir-finley-mrrgglton', 'small-time-buccaneer', 'southsea-deckhand', 'stonetusk-boar', 'swamp-dragon-egg', 'swamp-leech', 'swashburglar', 'tentacle-of-nzoth', 'timber-wolf', 'tournament-attendee', 'town-crier', 'tunnel-trogg', 'twilight-whelp', 'undertaker', 'vilefin-inquisitor', 'voidwalker', 'voodoo-doctor', 'warbot', 'wax-elemental', 'weasel-tunneler', 'webspinner', 'witchs-apprentice', 'witchwood-imp', 'worgen-infiltrator', 'wretched-tiller', 'young-dragonhawk', 'young-priestess', 'zealous-initiate', 'zombie-chow', 'murloc-tinyfin', 'snowflipper-penguin', 'target-dummy', 'wisp']

#The link to almost any minion in hearthhead is always http://www.hearthhead.com/cards/ followed by the minion's name (without any punctuation or capitalization and with all spaces replaced with -)
cardlinkstart = "http://www.hearthhead.com/cards/"
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
								the_card_link = '%s%s' % (cardlinkstart,card)
							elif card in dic_of_multiples:
								card = dic_of_multiples.get(card)
								the_card_link = '%s%s' % (cardlinkstart,card)
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
								the_card_link2 = '%s%s' % (cardlinkstart,card)
							elif card in dic_of_multiples:
								card = dic_of_multiples.get(card)
								the_card_link2 = '%s%s' % (cardlinkstart,card)
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
								the_card_link3 = '%s%s' % (cardlinkstart,card)
							elif card in dic_of_multiples:
								card = dic_of_multiples.get(card)
								the_card_link3 = '%s%s' % (cardlinkstart,card)
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
								the_card_link4 = '%s%s' % (cardlinkstart,card)
							elif card in dic_of_multiples:
								card = dic_of_multiples.get(card)
								the_card_link4 = '%s%s' % (cardlinkstart,card)
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
								the_card_link5 = '%s%s' % (cardlinkstart,card)
							elif card in dic_of_multiples:
								card = dic_of_multiples.get(card)
								the_card_link5 = '%s%s' % (cardlinkstart,card)
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
								the_card_link6 = '%s%s' % (cardlinkstart,card)
							elif card in dic_of_multiples:
								card = dic_of_multiples.get(card)
								the_card_link6 = '%s%s' % (cardlinkstart,card)
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
								the_card_link7 = '%s%s' % (cardlinkstart,card)
							elif card in dic_of_multiples:
								card = dic_of_multiples.get(card)
								the_card_link7 = '%s%s' % (cardlinkstart,card)
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
								the_card_link8 = '%s%s' % (cardlinkstart,card)
							elif card in dic_of_multiples:
								card = dic_of_multiples.get(card)
								the_card_link8 = '%s%s' % (cardlinkstart,card)
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
								the_card_link9 = '%s%s' % (cardlinkstart,card)
							elif card in dic_of_multiples:
								card = dic_of_multiples.get(card)
								the_card_link9 = '%s%s' % (cardlinkstart,card)
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
								the_card_link10 = '%s%s' % (cardlinkstart,card)
							elif card in dic_of_multiples:
								card = dic_of_multiples.get(card)
								the_card_link10 = '%s%s' % (cardlinkstart,card)
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
				#This is where the  message is made.  If both events and cards are not empty it will start making the message.  I used ifs instead of elifs, because elifs will only work once.
				#First it will find the link to the sound with SoundFinder.  #Then it will take the card's name, message about the type of line, and the link itself.
				#It is formatted into []() which is Reddit's way of having hyperlinks in comments.
				#In our example the_result would be "http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_EX1_165_Play_01.ogg" and then "Druid of the Claw's [play line.](the_result)" 
				if the_card != '' and the_event != '':
					the_result = SoundFinder(the_card_link,the_event)
					if the_result != None:
						print '''* %s\'s[%s](%s) 
		
		
''' % (the_card, event_caller, the_result)
						the_reply = '''* %s\'s[%s](%s) 
		
		
''' % (the_card, event_caller, the_result)
				if the_card2 != '' and the_event2 != '':
					the_result2 = SoundFinder(the_card_link2,the_event2)
					if the_result2 != None:
						print '''* %s\'s[%s](%s) 
		
		
''' % (the_card2, event_caller2, the_result2)
						the_reply2 = '''* %s\'s[%s](%s) 
		
		
''' % (the_card2, event_caller2, the_result2)
				if the_card3 != '' and the_event3 != '':
					the_result3 = SoundFinder(the_card_link3,the_event3)
					if the_result3 != None:
						print '''* %s\'s[%s](%s) 
		
		
''' % (the_card3, event_caller3, the_result3)
						the_reply3 = '''* %s\'s[%s](%s) 
		
		
''' % (the_card3, event_caller3, the_result3)
				if the_card4 != '' and the_event4 != '':
					the_result4 = SoundFinder(the_card_link4,the_event4)
					if the_result4 != None:
						print '''* %s\'s[%s](%s) 
		
		
''' % (the_card4, event_caller4, the_result4)
						the_reply4 = '''* %s\'s[%s](%s) 
		
		
''' % (the_card4, event_caller4, the_result4)
				if the_card5 != '' and the_event5 != '':
					the_result5 = SoundFinder(the_card_link5,the_event5)
					if the_result5 != None:
						print '''* %s\'s[%s](%s) 
		
		
''' % (the_card5, event_caller5, the_result5)
						the_reply5 = '''* %s\'s[%s](%s) 
		
		
''' % (the_card5, event_caller5, the_result5)
				if the_card6 != '' and the_event6 != '':
					the_result6 = SoundFinder(the_card_link6,the_event6)
					if the_result6 != None:
						print '''* %s\'s[%s](%s) 
		
		
''' % (the_card6, event_caller6, the_result6)
						the_reply6 = '''* %s\'s[%s](%s) 
		
		
''' % (the_card6, event_caller6, the_result6)
				if the_card7 != '' and the_event7 != '':
					the_result7 = SoundFinder(the_card_link7,the_event7)
					if the_result7 != None:
						print '''* %s\'s[%s](%s) 
		
		
''' % (the_card7, event_caller7, the_result7)
						the_reply7 = '''* %s\'s[%s](%s) 
		
		
''' % (the_card7, event_caller7, the_result7)
				if the_card8 != '' and the_event8 != '':
					the_result8 = SoundFinder(the_card_link8,the_event8)
					if the_result8 != None:
						print '''* %s\'s[%s](%s) 
		
		
''' % (the_card8, event_caller8, the_result8)
						the_reply8 = '''* %s\'s[%s](%s) 
		
		
''' % (the_card8, event_caller8, the_result8)
				if the_card9 != '' and the_event9 != '':
					the_result9 = SoundFinder(the_card_link9,the_event9)
					if the_result9 != None:
						print '''* %s\'s[%s](%s) 
		
		
''' % (the_card9, event_caller9, the_result9)
						the_reply9 = '''* %s\'s[%s](%s) 
		
		
''' % (the_card9, event_caller9, the_result9)
				if the_card10 != '' and the_event10 != '':
					the_result10 = SoundFinder(the_card_link10,the_event10)
					if the_result10 != None:
						print '''* %s\'s[%s](%s) 
		
		
''' % (the_card10, event_caller10, the_result10)
						the_reply10 = '''* %s\'s[%s](%s) 
		
		
''' % (the_card10, event_caller10, the_result10)
		
				#This is where the reply is created.  It checks out many replies are filled in by going from the last reply that would be filled in to the first reply.
				#When the amount of replies filled in is found, the program puts them all into a single reply called true_reply.  It then uses the PRAW reply command to send the reply off to Reddit. 
				if the_reply10 != '':
					true_reply = '%s%s%s%s%s%s%s%s%s%s' % (the_reply,the_reply2,the_reply3,the_reply4,the_reply5,the_reply6,the_reply7,the_reply8,the_reply9,the_reply10)
					comment.reply(true_reply)
				elif the_reply9 != '':
					true_reply = '%s%s%s%s%s%s%s%s%s' % (the_reply,the_reply2,the_reply3,the_reply4,the_reply5,the_reply6,the_reply7,the_reply8,the_reply9)
					comment.reply(true_reply)
				elif the_reply8 != '':
					true_reply = '%s%s%s%s%s%s%s%s' % (the_reply,the_reply2,the_reply3,the_reply4,the_reply5,the_reply6,the_reply7,the_reply8)
					comment.reply(true_reply)
				elif the_reply7 != '':
					true_reply = '%s%s%s%s%s%s%s' % (the_reply,the_reply2,the_reply3,the_reply4,the_reply5,the_reply6,the_reply7)
					comment.reply(true_reply)
				elif the_reply6 != '':
					true_reply = '%s%s%s%s%s%s' % (the_reply,the_reply2,the_reply3,the_reply4,the_reply5,the_reply6)
					comment.reply(true_reply)
				elif the_reply5 != '':
					true_reply = '%s%s%s%s%s' % (the_reply,the_reply2,the_reply3,the_reply4,the_reply5)
					comment.reply(true_reply)
				elif the_reply4 != '':
					true_reply = '%s%s%s%s' % (the_reply,the_reply2,the_reply3,the_reply4)
					comment.reply(true_reply)
				elif the_reply3 != '':
					true_reply = '%s%s%s' % (the_reply,the_reply2,the_reply3)
					comment.reply(true_reply)
				elif the_reply2 != '':
					true_reply = '%s%s' % (the_reply,the_reply2)
					comment.reply(true_reply)
				elif the_reply != '':
					true_reply = '%s' % (the_reply)
					comment.reply(true_reply)
		
				#These two if statments will reply a random precreated message to the common "good bot" and "bad bot" replies.  The if statment checks if a reply is one of the famous responses.
				#Then it will check the parent comment's author to check if the reply is aimed at the hearthsound_bot.
				#Then if it is, the bot will get a random number from randint and then choose a funny response to reply based off of the random number it gets.
				if text == 'good-bot':
					if comment.parent().author.name == secret.username:
						dice_roll = randint(1,4)
						if dice_roll == 1:
							comment.reply('*Great bot')
						elif dice_roll == 2:
							comment.reply('Shut up baby, I know it!')
						elif dice_roll == 3:
							comment.reply('And I love you, random citizen!')
						elif dice_roll == 4:
							comment.reply('The obvious conclusion.')
				if text == 'bad-bot':
					if comment.parent().author.name == secret.username:
						dice_roll = randint(1,4)
						if dice_roll == 1:
							comment.reply('Hearthsound_bot still not good bot?u punks are never satisfied are you?Hope you love being bitter because I definitely love being the greatest')
						elif dice_roll == 2:
							comment.reply('rank 25 player')
						elif dice_roll == 3:
							comment.reply('no u')
						elif dice_roll == 4:
							comment.reply('This is outrageous, it\'s unfair!')	
		
				#Here, all of the variables that could've been used are reset to blank as to avoid previous replies messing up future ones.
				#The cache is a list of all comments that have been replied to.  Since Reddit stream only reads the 100 latest comments I remove the 101st comment in the cache to free up space.
				cache.append(comment.id)
				if len(cache) == 101:
					cache.pop(100)
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
			except praw.exceptions.APIException as e:
				if e.error_type == 'RATELIMIT':
					error_time = re.search(r'[\d][\d]?',str(e))
					if error_time:
						time_error = '%s' % (error_time.group(0))
						time_error = int(time_error)
					error_mins = re.search(r'minute',str(e))
					if error_mins:
						time_error = time_error*60
					print e
					print 'waiting for %s seconds' % time_error
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
					time.sleep(time_error)
					print 'DONE SLEEPING'
					continue
			comment_list = []
			break