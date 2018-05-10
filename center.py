from sound_finder import SoundFinder
import re
#While most of the card sounds will have to be called by stating the card and type of sound, I plan to have a few famous sounds be called a bit eaiser.  Like the priest wow.
wow = "http://media.services.zam.com/v1/media/byName//hs/sounds/enus/VO_HERO_09_WOW_06.ogg"

#This is a list of all the minions currently in Hearthstone at the time of Witchwood.  It was made in card_list but copied into center so that the program doesn't have to remake the list each run.
minion_list = ['molten-giant', 'arcane-giant', 'clockwork-giant','mountain-giant', 'snowfury-giant', 'cthun', 'deathwing', 'deathwing-dragonlord', 'emeriss', 'faceless-behemoth', 'frost-giant',
  'kun-the-forgotten-king', 'nzoth-the-corruptor', 'sea-giant', 'tyrantus', 'ultrasaur', 'varian-wrynn', 'yogg-saron-hopes-end', 'yshaarj-rage-unbound', 'alexstrasza', 'anubarak', 'arch-thief-rafaam', 'aviana',
  'baku-the-mooneater', 'blade-of-cthun', 'blood-of-the-ancient-one', 'cenarius', 'dragoncaller-alanna','dragonhatcher', 'giant-mastodon', 'hadronox', 'icehowl', 'king-krush', 'king-mosh',
  'krul-the-unshackled', 'lord-jaraxxus', 'majordomo-executus', 'malganis', 'malygos', 'master-oakheart', 'mayor-noggenfogger', 'mekgineer-thermaplugg', 'nefarian', 'north-sea-kraken', 'nozdormu',
  'obsidian-statue', 'onyxia', 'ozruk', 'shudderwock', 'sleepy-dragon', 'soggoth-the-slitherer', 'voidlord', 'volcanqic-lumberer', 'ysera','alakir-the-windlord', 'anomalus', 'bonemare', 'cauldron-elemental',
  'charged-devilsaur', 'chromaggus', 'deranged-doctor', 'doomcaller', 'eldritch-horror', 'foe-reaper-4000', 'force-tank-max','fossilized-devilsaur', 'geosculptor-yip', 'giant-sand-worm', 'gilnean-royal-guard',
  'grand-archivist', 'grizzled-guardian', 'grommash-hellscream', 'gruul', 'ironbark-protector', 'kalimos-primal-lord','kathrena-winterwisp', 'kelthuzad', 'king-togwaggle', 'marin-the-fox',
  'medivh-the-guardian', 'primordial-drake', 'ragnaros-the-firelord', 'ragnaros-lightlord', 'rhonin', 'rotface', 'sindragosa','sneeds-old-shredder', 'splintergraft', 'splitting-festeroot', 'tess-greymane',
  'the-boogeymonster', 'the-lich-king', 'tirion-fordring', 'tortollan-primalist', 'violet-wurm', 'abominable-bowman','abyssal-enforcer', 'acidmaw', 'ancient-of-lore', 'ancient-of-war', 'hungry-ettin',
  'illidan-stormrage', 'iron-juggernaut', 'ivory-knight', 'jade-behemoth', 'justicar-trueheart', 'kabal-crystal-runner','kabal-trafficker', 'kidnapper', 'kodorider', 'lady-in-white', 'leatherclad-hogleader',
  'lord-of-the-arena', 'luckydo-buccaneer', 'madam-goya', 'maexxna', 'master-jouster', 'mech-bear-cat','menagerie-warden', 'moat-lurker', 'mogor-the-ogre', 'mogors-champion', 'moorabi', 'mossy-horror', 
  'mukla-tyrant-of-the-vale', 'mysterious-challenger', 'necrotic-geist', 'nerubian-prophet','nerubian-unraveler', 'ornery-direhorn', 'piloted-sky-golem', 'priestess-of-elune', 'reckless-rocketeer', 'reno-jackson', 'rin-the-first-disciple', 'sabretooth-stalker', 'savannah-highmane', 'scaled-nightmare', 'sea-reaver', 'seeping-oozeling', 'shieldmaiden', 'sideshow-spelleater', 'skeram-cultist', 'skulking-geist', 'spectral-pillager', 'spellweaver', 'spiteful-summoner', 'sunkeeper-tarim', 'sunwalker', 'sylvanas-windrunner', 'temple-enforcer', 'the-beast', 'the-black-knight', 'the-mistcaller', 'the-skeleton-knight', 'line-from-below', 'toki-time-tinker', 'toshley', 'trade-prince-gallywix', 'void-crusher', 'volcanic-drake', 'wilfred-fizzlebang', 'windfury-harpy', 'wind-up-burglebot', 'wobbling-runts', 'wrathion', 'abomination', 'alley-armorsmith', 'antique-healbot', 'anubisath-sentinel', 'arcane-tyrant', 'avian-watcher', 'azure-drake', 'bewitched-guardian', 'big-game-hunter', 'bittertide-hydra', 'blackwing-corruptor', 'blingtron-3000', 'blood-queen-lanathel', 'bloodworm', 'bolvar-fordragon', 'bolvar-fireblood', 'bomb-lobber', 'bomb-squad', 'bone-baron', 'bonfire-elemental', 'booty-bay-bodyguard', 'burgly-bully', 'captain-greenskin', 'carnivorous-cube', 'carrion-drake', 'chief-inspector', 'clockwork-automaton', 'clockwork-knight', 'cobalt-guardian', 'cobalt-scalebane', 'corpse-raiser', 'corpse-widow', 'corrosive-sludge', 'corrupted-healbot', 'crazed-worshipper', 'cryomancer', 'cult-apothecary', 'curio-collector', 'darius-crowley', 'dark-iron-skulker', 'darkscale-healer', 'darkshire-alchemist', 'darkspeaker', 'death-revenant', 'deathweb-spider', 'despicable-dreadlord', 'direhorn-hatchling', 'djinni-of-zephyrs', 'dollmaster-dorian', 'doomguard', 'doppelgangster', 'dragon-consort', 'drakonid-operative', 'druid-of-the-claw', 'druid-of-the-fang', 'duskfallen-aviana', 'earth-elemental', 'elise-the-trailblazer', 'elite-tauren-chieftain', 'ethereal-conjurer', 'ethereal-peddler', 'faceless-manipulator', 'fatespinner', 'fel-reaver', 'fen-creeper', 'festeroot-hulk', 'feugen', 'finja-the-flying-star', 'floating-watcher', 'frostwolf-warlord', 'fungalmancer', 'furbolg-mossbinder', 'ghostly-charger', 'glitter-moth', 'gloom-stag', 'green-jelly', 'grim-patron', 'grimestreet-enforcer', 'grook-fu-master', 'guild-recruiter', 'gurubashi-berserker', 'hallazeal-the-ascended', 'harrison-jones', 'hemet-nesingwary', 'ixlid-fungal-lord', 'junkbot', 'kabal-songstealer', 'king-of-beasts', 'knuckles', 'kvaldir-raider', 'leeroy-jenkins', 'loatheb', 'lotus-agents', 'lotus-assassin', 'lyra-the-sunshard', 'madder-bomber', 'menagerie-magician', 'mimirons-head', 'muck-hunter', 'muklas-champion', 'naga-sea-witch', 'nesting-roc', 'nexus-champion-saraad', 'nightblade', 'ogre-ninja', 'onyx-bishop', 'pit-fighter', 'possessed-lackey', 'prince-liam', 'prince-malchezaar', 'princess-huhuran', 'psych-o-tron', 'quartermaster', 'quartz-elemental', 'ram-wrangler', 'raza-the-chained', 'recruiter', 'red-mana-wyrm', 'rotten-applebaum', 'salty-dog', 'second-rate-bruiser', 'servant-of-kalimos', 'servant-of-yogg-saron', 'shado-pan-rider', 'shadowcaster', 'siege-engine', 'silver-hand-knight', 'skelemancer', 'sludge-belcher', 'spectral-knight', 'spiked-hogrider', 'spiteful-smith', 'stalagg', 'stampeding-kodo', 'starving-buzzard', 'stormpike-commando', 'stranglethorn-tiger', 'streetwise-investigator', 'summoning-stone', 'sunborne-valkyr', 'tar-lurker', 'thunder-bluff-valiant', 'tolvir-warden', 'tomb-lurker', 'trogg-gloomeater', 'tundra-rhino', 'tuskarr-jouster', 'twilight-darkmender', 'upgraded-repair-bot', 'usher-of-souls', 'validated-doomsayer', 'venomancer', 'venture-co-mercenary', 'verdant-longneck', 'vilebrood-skitterer', 'vilespine-slayer', 'virmen-sensei', 'voljin', 'voodoo-hexxer', 'white-eyes', 'windshear-stormcaller', 'witchwood-grizzly', 'aberrant-berserker', 'ancient-brewmaster', 'ancient-mage', 'ancient-shade', 'animated-armor', 'anubar-ambusher', 'arathi-weaponsmith', 'arcane-keysmith', 'arcane-nullifier-x-21', 'arcanosmith', 'arfus', 'armored-warhorse', 'arrogant-crusader', 'astral-tiger', 'auchenai-soulpriest', 'axe-flinger', 'backroom-bouncer', 'barnes', 'baron-rivendare', 'bellringer-sentry', 'blackwater-pirate', 'blood-witch', 'bloodhoof-brave', 'bright-eyed-scout', 'burly-rockjaw-trogg', 'chillblade-champion', 'chillwind-yeti', 'core-rager', 'corpsetaker', 'crowd-favorite', 'crystalweaver', 'cthuns-chosen', 'cult-master', 'cursed-disciple', 'cyclopian-horror', 'dalaran-aspirant', 'daring-reporter', 'dark-iron-dwarf', 'deathaxe-punisher', 'defender-of-argus', 'demented-frostcaller', 'dispatch-kodo', 'draenei-totemcarver', 'dragonkin-sorcerer', 'dragonling-mechanic', 'dread-corsair', 'dreadsteed', 'dunemaul-shaman', 'duskbreaker', 'eater-of-secrets', 'ebon-dragonsmith', 'eerie-statue', 'elise-starseeker', 'elven-minstrel', 'enhance-o-mechano', 'ethereal-arcanist', 'evil-heckler', 'evolved-kobold', 'exploding-bloatbat', 'faceless-shambler', 'faldorei-strider', 'fandral-staghelm', 'fel-cannon', 'felsoul-inquisitor', 'fire-plume-phoenix', 'fireguard-destroyer', 'flamewreathed-faceless', 'forest-guide', 'frigid-snobold', 'gentle-megasaur', 'genzo-the-shark', 'ghastly-conjurer', 'gnomish-inventor', 'goblin-blastmage', 'gorillabot-a-3', 'gormok-the-impaler', 'grave-shambler', 'grim-necromancer', 'grimy-gadgeteer', 'hoarding-dragon', 'holy-champion', 'hooded-acolyte', 'hooked-reaver', 'houndmaster', 'houndmaster-shaw', 'hozen-healer', 'hungry-dragon', 'infested-tauren', 'infested-wolf', 'ironwood-golem', 'jade-spirit', 'jeeves', 'jinyu-waterspeaker', 'jungle-moonkin', 'kabal-chemist', 'kazakus', 'keening-banshee', 'keeper-of-the-grove', 'keeper-of-uldaman', 'kezan-mystic', 'klaxxi-amber-weaver', 'kobold-illusionist', 'kobold-monk', 'kooky-chemist', 'korkron-elite', 'lakkari-felhound', 'leyline-manipulator', 'lifedrinker', 'lightfused-stegodon', 'lightspawn', 'lilian-voss', 'lost-tallstrider', 'lotus-illusionist', 'mad-hatter', 'magnataur-alpha', 'maiden-of-the-lake', 'master-of-disguise', 'master-of-evolution', 'meat-wagon', 'mechanical-yeti', 'midnight-drake', 'militia-commander', 'mini-mage', 'mire-keeper', 'mistwraith', 'mogushan-warden', 'murloc-knight', 'naga-corsair', 'night-howler', 'night-prowler', 'oasis-snapjaw', 'ogre-magi', 'old-murk-eye', 'phantom-freebooter', 'piloted-shredder', 'pit-lord', 'polluted-hoarder', 'priest-of-the-feast', 'prince-valanar', 'professor-putricide', 'rattling-rascal', 'ravenous-pterrordax', 'refreshment-vendor', 'rumbling-elemental', 'runeforge-haunter', 'sandbinder', 'saronite-chain-gang', 'savage-combatant', 'scaleworm', 'screwjank-clunker', 'seadevil-stinger', 'senjin-shieldmasta', 'shadow-sensei', 'shellshifter', 'sherazin-corpse-flower', 'shifting-shade', 'shimmering-courser', 'shroom-brewer', 'siltfin-spiritwalker', 'silvermoon-guardian', 'sneaky-devil', 'southsea-squidface', 'spawn-of-shadows', 'spellbreaker', 'spiritsinger-umbra', 'steam-surger', 'stegodon', 'stormwind-knight', 'strongshell-scavenger', 'summoning-portal', 'swift-messenger', 'tanaris-hogchopper', 'the-darkness', 'the-glass-knight', 'the-voraxx', 'ticking-abomination', 'tolvir-stoneshaper', 'tomb-pillager', 'tomb-spider', 'tortollan-shellraiser', 'totem-cruncher', 'tournament-medic', 'toxmonger', 'twilight-drake', 'twilight-guardian', 'twilight-summoner', 'unpowered-steambot', 'vex-crow', 'violet-teacher', 'voidcaller', 'wailing-soul', 'water-elemental', 'wee-spellstopper', 'wicked-skeleton', 'wicked-witchdoctor', 'wildwalker', 'windspeaker', 'witchwood-piper', 'worgen-greaser', 'xaril-poisoned-mind', 'acolyte-of-agony', 'acolyte-of-pain', 'addled-grizzly', 'alarm-o-bot', 'aldor-peacekeeper', 'amgam-rager', 'arcane-golem', 'argent-horserider', 'auctionmaster-beardo', 'backstreet-leper', 'bearshark', 'benevolent-djinn', 'black-cat', 'blackwald-pixie', 'blackwing-technician', 'blink-fox', 'blood-knight', 'bloodsail-cultist', 'blubber-baron', 'boisterous-bard', 'brann-bronzebeard', 'carrion-grub', 'cave-hydra', 'celestial-dreamer', 'chittering-tunneler', 'cloaked-huntress', 'coldlight-oracle', 'coldlight-seer', 'coldwraith', 'coliseum-manager', 'crypt-lord', 'curious-glimmerroot', 'cutthroat-buccaneer', 'dalaran-mage', 'dancing-swords', 'dark-cultist', 'darkshire-councilman', 'deadly-fork', 'deathlord', 'deathspeaker', 'demolisher', 'desert-camel', 'devilsaur-egg', 'disciple-of-cthun', 'doomed-apprentice', 'dragonhawk-rider', 'dragonslayer', 'drakkari-defender', 'drakkari-enchanter', 'dreadscale', 'druid-of-the-flame', 'druid-of-the-scythe', 'duskbat', 'duskhaven-hunter', 'earthen-ring-farseer', 'edwin-vancleef', 'eggnapper', 'elder-longneck', 'emperor-cobra', 'eydis-darkbane', 'face-collector', 'fel-orc-soulfiend', 'felguard', 'fencing-coach', 'fierce-monkey', 'fjola-lightbane', 'flamewaker', 'flesheating-ghoul', 'flying-machine', 'forlorn-stalker', 'froline-berserker', 'fungal-enchanter', 'giant-wasp', 'gilded-gargoyle', 'gluttonous-ooze', 'gnomeregan-infantry', 'gnomish-experimenter', 'goblin-sapper', 'greedy-sprite', 'grimestreet-pawnbroker', 'grimestreet-smuggler', 'grove-tender', 'happy-ghoul', 'harvest-golem', 'hench-clan-thug', 'hired-gun', 'hobgoblin', 'hot-spring-guardian', 'howlfiend', 'howling-commander', 'humongous-razorleaf', 'hyldnir-frostrider', 'ice-rager', 'igneous-elemental', 'illuminator', 'imp-gang-boss', 'imp-master', 'injured-blademaster', 'iron-sensei', 'ironbeak-owl', 'ironforge-rifleman', 'ironfur-grizzly', 'jungle-panther', 'kabal-courier', 'kabal-talonpriest', 'king-mukla', 'kirin-tor-mage', 'kobold-apprentice', 'kobold-barbarian', 'lights-champion', 'lil-exorcist', 'lone-champion', 'magma-rager', 'mana-tide-totem', 'manic-soulcaster', 'marsh-drake', 'master-of-ceremonies', 'metaltooth-leaper', 'mind-control-tech', 'mindbreaker', 'mirage-caller', 'moroes', 'mountainfire-armor', 'mounted-raptor', 'murloc-warleader', 'nightbane-templar', 'nightmare-amalgam', 'ogre-brute', 'orgrimmar-aspirant', 'pantry-spider', 'paragon-of-light', 'phantom-militia', 'plague-scientist', 'primalfin-lookout', 'prince-taldaram', 'pterrordax-hatchling', 'pumpkin-peasant', 'questing-adventurer', 'rabid-worgen', 'raging-worgen', 'raid-leader', 'rat-pack', 'ratcatcher', 'ravaging-ghoul', 'ravencaller', 'razorfen-hunter', 'rummaging-kobold', 'saboteur', 'scarlet-crusader', 'scarlet-purifier', 'sergeant-sally', 'sewer-crawler', 'shade-of-naxxramas', 'shadow-rager', 'shadowfiend', 'shady-dealer', 'shaku-the-collector', 'shaky-zipgunner', 'shallow-gravedigger', 'shattered-sun-cleric', 'shrieking-shroom', 'si-7-agent', 'silent-knight', 'silithid-swarmer', 'silver-hand-regent', 'silverback-patriarch', 'silverware-golem', 'sonya-shadowdancer', 'soot-spewer', 'southsea-captain', 'spawn-of-nzoth', 'spellslinger', 'spider-tank', 'squirming-tentacle', 'stablemaster', 'steward-of-darkshire', 'stitched-tracker', 'stonehill-defender', 'stoneskin-basilisk', 'stoneskin-gargoyle', 'street-trickster', 'tanglefur-mystic', 'tar-creeper', 'tauren-warrior', 'terrorscale-stalker', 'thrallmar-farseer', 'thunder-lizard', 'tinkertown-technician', 'tinkmaster-overspark', 'toothy-chest', 'toxic-sewer-ooze', 'tuskarr-totemic', 'twilight-acolyte', 'twilight-elder', 'twilight-flamecaller', 'unbound-elemental', 'unearthed-raptor', 'unlicensed-apothecary', 'valkyr-soulclaimer', 'vicious-fledgling', 'violet-illusionist', 'void-ripper', 'void-terror', 'voodoo-doll', 'vryghoul', 'walnut-sprite', 'warhorse-trainer', 'warsong-commander', 'wickerflame-burnbristle', 'witchs-cauldron', 'wolfrider', 'zola-the-gorgon', 'zoobot', 'acidic-swamp-ooze', 'alexstraszas-champion', 'amani-berserker', 'ancient-watcher', 'annoy-o-tron', 'anodized-robo-cub', 'arcanologist', 'archmage-arugal', 'argent-protector', 'argent-watchman', 'armorsmith', 'baleful-banker', 'beckoner-of-evil', 'bilefin-tidehunter', 'biteweed', 'bloodfen-raptor', 'bloodmage-thalnos', 'bloodsail-raider', 'blowgill-sniper', 'bluegill-warrior', 'boneguard-lieutenant', 'brrrloc', 'captains-parrot', 'cathedral-gargoyle', 'cavern-shinyfinder', 'clutchmother-zavas', 'cornered-sentry', 'crackling-razormaw', 'crazed-alchemist', 'cruel-taskmaster', 'cult-sorcerer', 'cutpurse', 'dark-peddler', 'darkshire-librarian', 'darnassus-aspirant', 'defias-ringleader', 'dire-wolf-alpha', 'dirty-rat', 'doomsayer', 'druid-of-the-saber', 'druid-of-the-swarm', 'drygulch-jailor', 'drywhisker-armorer', 'duskboar', 'echoing-ooze', 'eternal-sentinel', 'explosive-sheep', 'faerie-dragon', 'fallen-hero', 'fallen-sun-cleric', 'fire-plume-harbinger', 'flame-juggler', 'flametongue-totem', 'friendly-bartender', 'frostwolf-grunt', 'gadgetzan-ferryman', 'gadgetzan-socialite', 'garrison-commander', 'ghost-light-angler', 'gilblin-stalker', 'gnomeferatu', 'goblin-auto-barber', 'golakka-crawler', 'grimestreet-informant', 'grimestreet-outfitter', 'haunted-creeper', 'hobart-grapplehammer', 'huge-toad', 'hunting-mastiff', 'hydrologist', 'ice-walker', 'jade-swarmer', 'jeweled-scarab', 'kindly-grandmother', 'kings-elekk', 'knife-juggler', 'kobold-geomancer', 'kobold-hermit', 'lance-carrier', 'lightwell', 'loot-hoarder', 'lorewalker-cho', 'lost-spirit', 'mad-bomber', 'mad-scientist', 'mana-addict', 'mana-geode', 'mana-wraith', 'master-swordsmith', 'mechwarper', 'medivhs-valet', 'micro-machine', 'millhouse-manastorm', 'mistress-of-pain', 'murkspark-eel', 'murloc-tidehunter', 'murmuring-elemental', 'museum-curator', 'nat-pagle', 'nat-the-darkfisher', 'nerubar-weblord', 'nerubian-egg', 'netherspite-historian', 'novice-engineer', 'one-eyed-cheat', 'patient-assassin', 'pint-sized-summoner', 'plated-beetle', 'pompous-thespian', 'primalfin-champion', 'primalfin-totem', 'prince-keleseth', 'public-defender', 'puddlestomper', 'pyros', 'radiant-elemental', 'ravasaur-runt', 'raven-familiar', 'razorpetal-lasher', 'recombobulator', 'redband-wasp', 'river-crocolisk', 'rockpool-hunter', 'scavenging-hyena', 'scorp-o-matic', 'shadow-ascendant', 'shadowboxer', 'shielded-minibot', 'shimmering-tempest', 'ships-cannon', 'shrinkmeister', 'snowchugger', 'sorcerers-apprentice', 'sparring-partner', 'spellshifter', 'squashling', 'steamwheedle-sniper', 'stonesplinter-trogg', 'stubborn-gastropod', 'succubus', 'sunfury-protector', 'tainted-zealot', 'tiny-knight-of-evil', 'tortollan-forager', 'totem-golem', 'trogg-beastrager', 'tuskarr-fisherman', 'twilight-geomancer', 'twisted-worgen', 'undercity-huckster', 'undercity-valiant', 'unstable-ghoul', 'vicious-scalehide', 'vitality-totem', 'volatile-elemental', 'vulgar-homunculus', 'whirling-zap-o-matic', 'wild-pyromancer', 'wrathguard', 'wyrmrest-agent', 'youthful-brewmaster', 'abusive-sergeant', 'acherus-veteran', 'air-elemental', 'alleycat', 'angry-chicken', 'animated-berserker', 'arcane-anomaly', 'arcane-artificer', 'argent-squire', 'babbling-book', 'bladed-cultist', 'blood-imp', 'bloodsail-corsair', 'brave-archer', 'buccaneer', 'chameleos', 'clockwork-gnome', 'cogmaster', 'crystalline-oracle', 'deadscale-knight', 'dire-mole', 'dragon-egg', 'dust-devil', 'elven-archer', 'emerald-hive-queen', 'emerald-reaver', 'enchanted-raven', 'feral-gibberer', 'fiery-bat', 'fire-fly', 'flame-imp', 'forbidden-ancient', 'gadgetzan-jouster', 'glacial-shard', 'goldshire-footman', 'gravelsnout-knight', 'grimscale-chum', 'grimscale-oracle', 'hungry-crab', 'injured-kvaldir', 'jeweled-macaw', 'kabal-lackey', 'kobold-librarian', 'leper-gnome', 'lightwarden', 'lowly-squire', 'malchezaars-imp', 'mana-wyrm', 'meanstreet-marshal', 'mistress-of-mixtures', 'murloc-raider', 'murloc-tidecaller', 'northshire-cleric', 'nzoths-first-mate', 'patches-the-pirate', 'pit-snake', 'possessed-villager', 'raptor-hatchling', 'reliquary-seeker', 'righteous-protector', 'runic-egg', 'sanguine-reveler', 'secretkeeper', 'selfless-hero', 'shadowbomber', 'shieldbearer', 'shifter-zerus', 'sir-finley-mrrgglton', 'small-time-buccaneer', 'southsea-deckhand', 'stonetusk-boar', 'swamp-dragon-egg', 'swamp-leech', 'swashburglar', 'tentacle-of-nzoth', 'timber-wolf', 'tournament-attendee', 'town-crier', 'tunnel-trogg', 'twilight-whelp', 'undertaker', 'vilefin-inquisitor', 'voidwalker', 'voodoo-doctor', 'warbot', 'wax-elemental', 'weasel-tunneler', 'webspinner', 'witchs-apprentice', 'witchwood-imp', 'worgen-infiltrator', 'wretched-tiller', 'young-dragonhawk', 'young-priestess', 'zealous-initiate', 'zombie-chow', 'murloc-tinyfin', 'snowflipper-penguin', 'target-dummy', 'wisp']
#The link to any minion in hearthhead is always http://www.hearthhead.com/cards/ followed by the minion's name (without any punctuation or capitalization and with all spaces replaced with -)
cardlinkstart = "http://www.hearthhead.com/cards/"

#The EventFinder looks at the event lines that are given for a link, and returns a message that is a bit better to read.
def EventFinder(line_type):
	event = ['\'s play line.', '\'s attack line.', '\'s death line', '\'s trigger line']
	if line_type == 'play':
		return '\'s play line.'
	elif line_type == 'attack':
		return '\'s attack line.'
	elif line_type == 'death':
		return '\'s death line.'
	elif line_type == 'trigger':
		return '\'s trigger line.'

#The event list is a list of the terms people can use to call the bot and decide the type of line they want.
event_list = ['((play))','((attack))','((death))','((trigger))']

#These are empty variables that will be used later.
the_card = ''
the_event = ''
the_card2 = ''
the_event2 = ''
the_card3 = ''
the_event3 = ''
the_card4 = ''
the_event4 = ''
the_card5 = ''
the_event5 = ''
the_card6 = ''
the_event6 = ''
the_card7 = ''
the_event7 = ''
the_card8 = ''
the_event8 = ''
the_card9 = ''
the_event9 = ''
the_card10 = ''
the_event10 = ''

#This list is a placeholder for actual comments
comments = ['((lord-jaraxxus))','iron-juggernautwasdfaw','((play))','bolvar-fireblood', '((attack))','((death))','nexus-champion-saraad','((trigger))']

#This will check each individual comment in a list of comments(for comment in comments), and then check if that comment has a card in it(for card in minion list, if card in comment).
#If it does it will find the card link and store the link and card in the variable the_card#(cardlinkstart and the_card#).
#Each individual card is kept in its own the_card# variable so 10 cards in total can be called in a single comment.
#To make sure no cards are overwritten, it checks if each the_card# is blank, and uses the first blank the_card# variable it finds. 
for comment in comments:
	for card in minion_list:
			if card in comment:
				if the_card == '':
					the_card_link = '%s%s' % (cardlinkstart,card)
					the_card = card
				elif the_card2 == '':
					the_card_link2 = '%s%s' % (cardlinkstart,card)
					the_card2 = card
				elif the_card3 == '':
					the_card_link3 = '%s%s' % (cardlinkstart,card)
					the_card3 = card
				elif the_card4 == '':
					the_card_link4 = '%s%s' % (cardlinkstart,card)
					the_card4 = card
				elif the_card5 == '':
					the_card_link5 = '%s%s' % (cardlinkstart,card)
					the_card5 = card
				elif the_card6 == '':
					the_card_link6 = '%s%s' % (cardlinkstart,card)
					the_card6 = card
				elif the_card7 == '':
					the_card_link7 = '%s%s' % (cardlinkstart,card)
					the_card7 = card
				elif the_card8 == '':
					the_card_link8 = '%s%s' % (cardlinkstart,card)
					the_card8 = card
				elif the_card9 == '':
					the_card_link9 = '%s%s' % (cardlinkstart,card)
					the_card9 = card
				elif the_card10 == '':
					the_card_link10 = '%s%s' % (cardlinkstart,card)
					the_card10 = card

#This does exactly the same as the cards.  The two differnces are that the first and last two characters of the_event are being trimmed off.
#This is because the events need to be called with double parenthesis, and the reason for that is to try to avoid unwanted callings of the bot.  The second thing that is different is the event_caller.
for comment in comments:
	for line in event_list:
		if line in comment:
			if the_event == '':
				the_event = line[2:len(line)-2]
				event_caller = EventFinder(the_event)
			elif the_event2 == '':
				the_event2 = line[2:len(line)-2]
				event_caller2 = EventFinder(the_event2)
			elif the_event3 == '':
				the_event3 = line[2:len(line)-2]
				event_caller3 = EventFinder(the_event3)
			elif the_event4 == '':
				the_event4 = line[2:len(line)-2]
				event_caller4 = EventFinder(the_event4)
			elif the_event5 == '':
				the_event5 = line[2:len(line)-2]
				event_caller5 = EventFinder(the_event5)
			elif the_event6 == '':
				the_event6 = line[2:len(line)-2]
				event_caller6 = EventFinder(the_event6)
			elif the_event7 == '':
				the_event7 = line[2:len(line)-2]
				event_caller7 = EventFinder(the_event7)
			elif the_event8 == '':
				the_event8 = line[2:len(line)-2]
				event_caller8 = EventFinder(the_event8)
			elif the_event9 == '':
				the_event9 = line[2:len(line)-2]
				event_caller9 = EventFinder(the_event9)
			elif the_event10 == '':
				the_event10 = line[2:len(line)-2]
				event_caller10 = EventFinder(the_event10)

#This is where the actual message is made.  If both events and cards are not empty it will start making the message.  I used ifs instead of elifs, because elifs will only work once.
#First it will find the link to the sound with SoundFinder.  #Then it will take the card's name, message about the type of line, and the link itself.
#It is formatted into []() which is Reddit's way of having hyperlinks in comments. 
if the_card != '' and the_event != '':
	the_result = SoundFinder(the_card_link,the_event)
	print '[%s%s](%s)' % (the_card, event_caller, the_result)
if the_card2 != '' and the_event2 != '':
	the_result2 = SoundFinder(the_card_link2,the_event2)
	print '[%s%s](%s)' % (the_card2, event_caller2, the_result2)
if the_card3 != '' and the_event3 != '':
	the_result3 = SoundFinder(the_card_link3,the_event3)
	print '[%s%s](%s)' % (the_card3, event_caller3, the_result3)
if the_card4 != '' and the_event4 != '':
	the_result4 = SoundFinder(the_card_link4,the_event4)
	print '[%s%s](%s)' % (the_card4, event_caller4, the_result4)
if the_card5 != '' and the_event5 != '':
	the_result5 = SoundFinder(the_card_link5,the_event5)
	print '[%s%s](%s)' % (the_card5, event_caller5, the_result5)
if the_card6 != '' and the_event6 != '':
	print SoundFinder(the_card6,the_event6)
	the_result6 = SoundFinder(the_card_link6,the_event6)
	print '[%s%s](%s)' % (the_card6, event_caller6, the_result6)
if the_card7 != '' and the_event7 != '':
	the_result7 = SoundFinder(the_card_link7,the_event7)
	print '[%s%s](%s)' % (the_card7, event_caller7, the_result7)
if the_card8 != '' and the_event8 != '':
	the_result8 = SoundFinder(the_card_link8,the_event8)
	print '[%s%s](%s)' % (the_card8, event_caller8, the_result8)
if the_card9 != '' and the_event9 != '':
	the_result9 = SoundFinder(the_card_link9,the_event9)
	print '[%s%s](%s)' % (the_card9, event_caller9, the_result9)
if the_card10 != '' and the_event10 != '':
	the_result10 = SoundFinder(the_card_link10,the_event10)
	print '[%s%s](%s)' % (the_card10, event_caller10, the_result10)