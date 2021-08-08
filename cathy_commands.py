from cathy_config import *
import subprocess, asyncio, discord, random, math, socket, os, io, PIL, aiohttp
import hashlib
from datetime import datetime, timedelta
from PIL import Image, ImageFilter, ImageOps

# Other scripts
from not_constantinople import generate_provinces, generate_settlements
from deeppyer import deepfry
from rotpixels import rotpixels
from transparentgif import save_transparent_gif
from unicornavatar import create_avatar
from color_cuber import color_cuber
from contourperlin import random_islands

# For random emoji
from itertools import accumulate
from bisect import bisect
from random import randrange
from unicodedata import name as unicode_name

# Just one for now
voice_clients = {}

EMOJI_RANGES_UNICODE = {
    6: [
        ('\U0001F300', '\U0001F320'),
        ('\U0001F330', '\U0001F335'),
        ('\U0001F337', '\U0001F37C'),
        ('\U0001F380', '\U0001F393'),
        ('\U0001F3A0', '\U0001F3C4'),
        ('\U0001F3C6', '\U0001F3CA'),
        ('\U0001F3E0', '\U0001F3F0'),
        ('\U0001F400', '\U0001F43E'),
        ('\U0001F440', ),
        ('\U0001F442', '\U0001F4F7'),
        ('\U0001F4F9', '\U0001F4FC'),
        ('\U0001F500', '\U0001F53C'),
        ('\U0001F540', '\U0001F543'),
        ('\U0001F550', '\U0001F567'),
        ('\U0001F5FB', '\U0001F5FF')
    ],
    7: [
        ('\U0001F300', '\U0001F32C'),
        ('\U0001F330', '\U0001F37D'),
        ('\U0001F380', '\U0001F3CE'),
        ('\U0001F3D4', '\U0001F3F7'),
        ('\U0001F400', '\U0001F4FE'),
        ('\U0001F500', '\U0001F54A'),
        ('\U0001F550', '\U0001F579'),
        ('\U0001F57B', '\U0001F5A3'),
        ('\U0001F5A5', '\U0001F5FF')
    ],
    8: [
        ('\U0001F300', '\U0001F579'),
        ('\U0001F57B', '\U0001F5A3'),
        ('\U0001F5A5', '\U0001F5FF')
    ]
}

def random_emoji(unicode_version = 6):
    if unicode_version in EMOJI_RANGES_UNICODE:
        emoji_ranges = EMOJI_RANGES_UNICODE[unicode_version]
    else:
        emoji_ranges = EMOJI_RANGES_UNICODE[-1]

    # Weighted distribution
    count = [ord(r[-1]) - ord(r[0]) + 1 for r in emoji_ranges]
    weight_distr = list(accumulate(count))

    # Get one point in the multiple ranges
    point = randrange(weight_distr[-1])

    # Select the correct range
    emoji_range_idx = bisect(weight_distr, point)
    emoji_range = emoji_ranges[emoji_range_idx]

    # Calculate the index in the selected range
    point_in_range = point
    if emoji_range_idx != 0:
        point_in_range = point - weight_distr[emoji_range_idx - 1]

    # Emoji 😄
    emoji = chr(ord(emoji_range[0]) + point_in_range)
    emoji_name = unicode_name(emoji, '(No name found for this codepoint)').capitalize()
    emoji_codepoint = "U+{}".format(hex(ord(emoji))[2:].upper())

    return (emoji, emoji_codepoint, emoji_name)

many_verbs = [
"abide","accelerate","accept","accomplish","achieve","acquire","acted","activate","adapt","add","address","administer","admire","admit","adopt","advise","afford","agree","alert","alight","allow","altered","amuse","analyze","announce","annoy","answer","anticipate","apologize","appear","applaud","applied","appoint","appraise","appreciate","approve","arbitrate","argue","arise","arrange","arrest","arrive","ascertain","ask","assemble","assess","assist","assure","attach","attack","attain","attempt","attend","attract","audited","avoid","awake","back","bake","balance","ban","bang","bare","bat","bathe","battle","be","beam","bear","beat","become","beg","begin","behave","behold","belong","bend","beset","bet","bid","bind","bite","bleach","bleed","bless","blind","blink","blot","blow","blush","boast","boil","bolt","bomb","book","bore","borrow","bounce","bow","box","brake","branch","break","breathe","breed","brief","bring","broadcast","bruise","brush","bubble","budget","build","bump","burn","burst","bury","bust","buy","buzz","calculate","call","camp","care","carry","carve","cast","catalog","catch","cause","challenge","change","charge","chart","chase","cheat","check","cheer","chew","choke","choose","chop","claim","clap","clarify","classify","clean","clear","cling","clip","close","clothe","coach","coil","collect","color","comb","come","command","communicate",
"compare","compete","compile","complain","complete","compose","compute","conceive","concentrate","conceptualize","concern","conclude","conduct","confess","confront","confuse","connect","conserve","consider","consist","consolidate","construct","consult","contain","continue","contract","control","convert","coordinate","copy","correct","correlate","cost","cough","counsel","count","cover","crack","crash","crawl","create","creep","critique","cross","crush","cry","cure","curl","curve","cut","cycle","dam","damage","dance","dare","deal","decay","deceive","decide","decorate","define","delay","delegate","delight","deliver","demonstrate","depend","describe","desert","deserve","design","destroy","detail","detect","determine","develop","devise","diagnose","dig","direct","disagree","disappear","disapprove","disarm","discover","dislike","dispense","display","disprove","dissect","distribute","dive","divert","divide","do","double","doubt","draft","drag","drain","dramatize","draw","dream","dress","drink","drip","drive","drop","drown","drum","dry","dust","dwell","earn","eat","edited","educate","eliminate","embarrass","employ","empty","enacted","encourage","end","endure","enforce","engineer","enhance","enjoy","enlist","ensure","enter","entertain","escape","establish","estimate","evaluate","examine","exceed","excite","excuse","execute","exercise","exhibit","exist",
"expand","expect","expedite","experiment","explain","explode","express","extend","extract","face","facilitate","fade","fail","fancy","fasten","fax","fear","feed","feel","fence","fetch","fight","file","fill","film","finalize","finance","find","fire","fit","fix","flap","flash","flee","fling","float","flood","flow","flower","fly","fold","follow","fool","forbid","force","forecast","forego","foresee","foretell","forget","forgive","form","formulate","forsake","frame","freeze","frighten","fry","gather","gaze","generate","get","give","glow","glue","go","govern","grab","graduate","grate","grease","greet","grin","grind","grip","groan","grow","guarantee","guard","guess","guide","hammer","hand","handle","handwrite","hang","happen","harass","harm","hate","haunt","head","heal","heap","hear","heat","help","hide","hit","hold","hook","hop","hope","hover","hug","hum","hunt","hurry","hurt","hypothesize","identify","ignore","illustrate","imagine","implement","impress","improve","improvise","include","increase","induce","influence","inform","initiate","inject","injure","inlay","innovate","input","inspect","inspire","install","institute","instruct","insure","integrate","intend","intensify","interest","interfere","interlay","interpret","interrupt","interview","introduce","invent","inventory","investigate","invite","irritate","itch","jail","jam","jog","join","joke",
"judge","juggle","jump","justify","keep","kept","kick","kill","kiss","kneel","knit","knock","knot","know","label","land","last","laugh","launch","lay","lead","lean","leap","learn","leave","lecture","led","lend","let","level","license","lick","lie","lifted","light","lighten","like","list","listen","live","load","locate","lock","log","long","look","lose","love","maintain","make","man","manage","manipulate","manufacture","map","march","mark","market","marry","match","mate","matter","mean","measure","meddle","mediate","meet","melt","melt","memorize","mend","mentor","milk","mine","mislead","miss","misspell","mistake","misunderstand","mix","moan","model","modify","monitor","moor","motivate","mourn","move","mow","muddle","mug","multiply","murder","nail","name","navigate","need","negotiate","nest","nod","nominate","normalize","note","notice","number","obey","object","observe","obtain","occur","offend","offer","officiate","open","operate","order","organize","oriented","originate","overcome","overdo","overdraw","overflow","overhear",
"overtake","overthrow","owe","own","pack","paddle","paint","park","part","participate","pass","paste","pat","pause","pay","peck","pedal","peel","peep","perceive","perfect","perform","permit","persuade","phone","photograph","pick","pilot","pinch","pine","pinpoint","pioneer","place","plan","plant","play","plead","please","plug","point","poke","polish","pop","possess","post","pour","practice","praised","pray","preach","precede","predict","prefer","prepare","prescribe","present","preserve","preset","preside","press","pretend","prevent","prick","print","process","procure","produce","profess","program","progress","project","promise","promote","proofread","propose","protect","prove","provide","publicize","pull","pump","punch","puncture","punish","purchase","push","put","qualify","question","queue","quit","race","radiate","rain","raise","rank","rate","reach","read","realign","realize","reason","receive","recognize","recommend","reconcile","record","recruit","reduce","refer","reflect","refuse","regret","regulate","rehabilitate","reign",
"reinforce","reject","rejoice","relate","relax","release","rely","remain","remember","remind","remove","render","reorganize","repair","repeat","replace","reply","report","represent","reproduce","request","rescue","research","resolve","respond","restored","restructure","retire","retrieve","return","review","revise","rhyme","rid","ride","ring","rinse","rise","risk","rob","rock","roll","rot","rub","ruin","rule","run","rush","sack","sail","satisfy","save","saw","say","scare","scatter","schedule","scold","scorch","scrape","scratch","scream","screw","scribble","scrub","seal","search","secure","see","seek","select","sell","send","sense","separate","serve","service","set","settle","sew","shade","shake","shape","share","shave","shear","shed","shelter","shine","shiver","shock","shoe","shoot","shop","show","shrink","shrug","shut","sigh","sign","signal","simplify","sin","sing","sink","sip","sit","sketch","ski","skip","slap","slay","sleep","slide","sling","slink","slip","slit","slow","smash","smell","smile","smite","smoke","snatch","sneak","sneeze","sniff","snore","snow","soak","solve",
"soothe","soothsay","sort","sound","sow","spare","spark","sparkle","speak","specify","speed","spell","spend","spill","spin","spit","split","spoil","spot","spray","spread","spring","sprout","squash","squeak","squeal","squeeze","stain","stamp","stand","stare","start","stay","steal","steer","step","stick","stimulate","sting","stink","stir","stitch","stop","store","strap","streamline","strengthen","stretch","stride","strike","string","strip","strive","stroke","structure","study","stuff","sublet","subtract","succeed","suck","suffer","suggest","suit","summarize","supervise","supply","support","suppose","surprise","surround","suspect","suspend","swear","sweat","sweep","swell","swim","swing","switch","symbolize","synthesize","systemize","tabulate","take","talk","tame","tap","target","taste","teach","tear","tease","telephone","tell","tempt","terrify","test","thank","thaw","think","thrive","throw","thrust","tick","tickle","tie","time","tip","tire","touch","tour","tow","trace","trade","train","transcribe","transfer","transform","translate","transport","trap","travel","tread","treat","tremble","trick","trip","trot","trouble","troubleshoot","trust","try","tug","tumble","turn","tutor","twist",
"type","undergo","understand","undertake","undress","unfasten","unify","unite","unlock","unpack","untidy","update","upgrade","uphold","upset","use","utilize","vanish","verbalize","verify","vex","visit","wail","wait","wake","walk","wander","want","warm","warn","wash","waste","watch","water","wave","wear","weave","wed","weep","weigh","welcome","wend","wet","whine","whip","whirl","whisper","whistle","win","wind","wink","wipe","wish","withdraw","withhold","withstand","wobble","wonder","work","worry","wrap","wreck","wrestle","wriggle","wring","write","x-ray","yawn","yell","zip","zoom"
]

many_nouns = [
"ball","bat","bed","book","boy","bun","can","cake","cap","car","cat","cow","cub","cup","dad","day","dog","doll","dust","fan","feet","girl","gun","hall","hat","hen","jar","kite","man","map","men","mom","pan","pet","pie","pig","pot","rat","son","sun","toe","tub","van","apple","arm","banana","bike","bird","book","chin","clam","class","clover","club","corn","crayon","crow","crown","crowd","crib","desk","dime","dirt","dress","fang","field","flag","flower","fog","game","heat","hill","home","horn","hose","joke","juice","kite","lake","maid","mask","mice","milk","mint","meal","meat","moon","mother","morning","name","nest","nose","pear","pen","pencil","plant","rain","river","road","rock","room","rose","seed","shape","shoe","shop","show","sink","snail","snake","snow","soda","sofa","star","step","stew","stove","straw","string","summer","swing","table","tank","team","tent","test","toes","tree","vest","water","wing","winter","alarm","animal","aunt","bait","balloon","bath","bead","beam","bean","bedroom","boot","bread","brick","brother","camp","chicken","children","crook","deer","dock","doctor","downtown","drum","dust","eye","family","father","fight","flesh","food","frog","goose","grade",
"grandfather","grandmother","grape","grass","hook","horse","jail","jam","kiss","kitten","light","loaf","lock","lunch","lunchroom","meal","mother","notebook","owl","pail","parent","park","plot","rabbit","rake","robin","sack","sail","scale","sea","sister","soap","song","spark","space","spoon","spot","spy","summer","tiger","toad","town","trail","tramp","tray","trick","trip","uncle","vase","winter","water","week","wheel","wish","wool","yard","zebra","actor","airplane","airport","army","baseball","beef","birthday","boy","brush","bushes","butter ","cast","cave","cent","cherries","cherry","cobweb","coil","cracker","dinner","eggnog","elbow","face","fireman","flavor","gate","glove","glue","goldfish","goose","grain","hair","haircut","hobbies","holiday","hot","jellyfish","ladybug","mailbox","number","oatmeal","pail","pancake","pear","pest","popcorn","queen","quicksand","quiet","quilt","rainstorm","scarecrow","scarf","stream","street","sugar","throne","toothpaste","twig","volleyball","wood","wrench","advice","anger","answer","apple","arithmetic","badge","basket","basketball","battle","beast","beetle","beggar","brain","branch","bubble","bucket","cactus","cannon","cattle","celery","cellar","cloth","coach","coast","crate","cream","daughter","donkey","drug","earthquake","feast","fifth","finger","flock","frame","furniture","geese","ghost","giraffe","governor","honey","hope","hydrant","icicle","income","island","jeans","judge","lace","lamp","lettuce","marble","month","north","ocean","patch","plane","playground","poison","riddle","rifle","scale","seashore","sheet","sidewalk","skate","slave","sleet","smoke","stage","station","thrill","throat","throne","title","toothbrush","turkey",
"underwear","vacation","vegetable","visitor","voyage","year","able","achieve","acoustics","action","activity","aftermath","afternoon","afterthought","apparel","appliance","beginner","believe","bomb","border","boundary","breakfast","cabbage","cable","calculator","calendar","caption","carpenter","cemetery","channel","circle","creator","creature","education","faucet","feather","friction","fruit","fuel","galley","guide","guitar","health","heart","idea","kitten","laborer","language","lawyer","linen","locket","lumber","magic","minister","mitten","money","mountain","music","partner","passenger",
"pickle","picture","plantation","plastic","pleasure","pocket","police","pollution","railway","recess","reward","route","scene","scent","squirrel","stranger","suit","sweater","temper","territory","texture","thread","treatment","veil","vein","volcano","wealth","weather","wilderness","wren","wrist","writerable","achieve","acoustics","action","activity","aftermath","afternoon","afterthought","apparel","appliance","beginner","believe","bomb","border","boundary","breakfast","cabbage","cable","calculator","calendar","caption","carpenter","cemetery","channel","circle","creator","creature","education","faucet","feather","friction","fruit","fuel","galley","guide","guitar","health","heart","idea","kitten","laborer","language","lawyer","linen","locket","lumber","magic","minister","mitten","money","mountain","music","partner","passenger","pickle","picture","plantation","plastic","pleasure","pocket","police","pollution","railway","recess","reward","route","scene","scent","squirrel","stranger","suit","sweater","temper","territory","texture","thread","treatment","veil","vein","volcano","wealth","weather","wilderness","wren","wrist","writer","fox"
]


def temp_file(name):
	return '/home/pi/junk/'+name

def run_squirrel(text):
	file = open(temp_file('code.nut'), 'w') 
	file.write(text)
	file.close()
	return subprocess.Popen('/home/pi/bin/custom_sq '+temp_file('code.nut'), shell=True, stdout=subprocess.PIPE).stdout.read().decode()

def bytes_from_file(name):
	try:
		file = open(temp_file(name), 'rb') 
		data = file.read(100)
		file.close()
		output = ''
		for b in data:
			output += '%.2X ' % b
		return output
	except Exception:
		return "Couldn't open output file"

def remove_file(name):
	try:
		os.remove(filename)
	except Exception:
		pass

def monospace(text):
	return {'text': text, 'markdown': '```\n'+text+'\n```'}

def date_from_string(text):
	today = datetime.today()
	split = text.split('/')

	if len(split) == 2:
		return datetime(today.year, int(split[0]), int(split[1]))

	if len(split) == 3:
		return datetime(int(split[2]), int(split[0]), int(split[1]))

	# give up and use the current date
	return datetime(today.year, today.month, today.day)

def padImage(image, x, y, padToW, padToH):
	i = Image.new('RGBA', (padToW, padToH), (0, 0, 0, 0))
	i.paste(image, (x, y))
	return i

command_handlers = {}	# dictionary of functions to call for each command
command_aliases = {}	# dictionary of commands to change to other commands
command_categories = {}	# categories
command_about = {}		# help text
command_syntax = {}		# help text
threaded_commands = set()

def bot_command(alias=[], category="Miscellaneous", hidden=False, about=None, syntax=None, threaded=False):
	def decorator(f):
		command_name = f.__name__[3:]
		command_handlers[command_name] = f
		if not hidden:
			if category not in command_categories:
				command_categories[category] = set()
			command_categories[category].add(command_name)
		if about:
			command_about[command_name] = about
		if syntax:
			command_syntax[command_name] = syntax
		for a in alias:
			command_aliases[a] = command_name
		if threaded:
			threaded_commands.add(command_name)
	return decorator

# COMMAND HANDLERS STARTS HERE

@bot_command(category="Text")
async def fn_echo(arg, p):
	return {'text': arg}

@bot_command(category="Programming")
async def fn_sq(arg, p):
	return {'text': run_squirrel(arg)}
command_aliases['squirrel'] = 'sq'

@bot_command(category="Programming")
async def fn_calc(arg, p):
	return {'text': run_squirrel('print(%s)' % arg)}

@bot_command(category="Text")
async def fn_titlecase(arg, p):
	return {'text': arg.title()}

@bot_command(category="Text")
async def fn_uppercase(arg, p):
	return {'text': arg.upper()}

@bot_command(category="Text")
async def fn_lowercase(arg, p):
	return {'text': arg.lower()}

@bot_command(category="Text")
async def fn_swapcase(arg, p):
	return {'text': arg.swapcase()}

@bot_command(category="Random")
async def fn_random(arg, p):
	param = arg.split(' ')
	if len(param) != 2:
		return {'text': 'Syntax: random min max'}
	else:
		minimum = int(param[0])
		maximum = int(param[1])
		return {'text': str(random.randint(minimum, maximum))}

@bot_command(category="Random")
async def fn_choice(arg, p):
	choices = arg.split('/')
	return {'text': random.choice(choices)}
command_aliases['choices'] = 'choice'
command_aliases['choose'] = 'choice'

@bot_command(category="Random")
async def fn_altonbrownfact(arg, p):
	facts = ["#1. Alton Brown grinds his own peppercorns. With his teeth.", "#2. Alton Brown's chili cheese fries are healthier than raw carrots. Even after he adds the bacon and lard.", "#3. Alton Brown brushes his teeth with wasabi and gargles with pickle brine. But still his breath smells like lemon merengue.", "#4. Alton Brown can boil a three-minute egg in thirty-seven seconds.", "#5. When Alton Brown was born, he collected the hospital slop they'd left for his mother and made it into an zesty, appetizing goulash. The dish fed the entire maternity ward for a week.", "#6. In the first, as-yet-unaired episode of Iron Chef America, Alton Brown single-handedly defeated an all-star team of Bobby Flay, Cat Cora, and Hiroyuki Sakai. The secret ingredient was 'whimsy'.", "#7. Alton Brown doesn't reduce sauces. He demoralizes sauces.", "#8. Alton Brown prepares his fugu blindfolded, with one chopstick and a plastic spork. Alton Brown ain't afraid of no chump neurotoxin.", "#9. Alton Brown's blender has four speeds: 'stir', 'mix', 'frappe', and 'plasmify'.", "#10. Alton Brown can split a pineapple in half using only his pinkies. For coconuts, though, he has to use his thumbs.", "#11. Alton Brown knows where capers come from. And he grows his own, on a Chia pet in the pantry.", "#12. On Rachel Ray's show, she shows people where to eat for less than forty dollars a day. When Alton Brown eats, people pay him.", "#13. Alton Brown slices ham so thin, it can only be seen using an electron microscope.", "#14. Some knives can slice through a tin can and still cut a tomato. Alton Brown's knives can slice through a Pontiac, and still cut a tin can.", "#15. Grown men have been known to weep for joy in the mere presence of Alton Brown's vinagrette. His hollandaise sauce can kill a man from sheer ecstacy at forty paces.", "#16. Alton Brown can eat just one Lay's potato chip. If he ever bothered to eat food he didn't make himself, that is.", "#17. Alton Brown once got carried away slicing carrots, and julienned his cutting board. Undaunted, he sauteed the splinters in olive oil and spices -- and they were delicious.", "#18. Every Burger King Alton Brown has walked into has immediately closed forever -- try as they might, they simply can't 'do it his way'.", "#19. Alton Brown can pair a wine with any food -- including hot dogs, ice cream, raw eggs, Alpo, sawdust, and soylent green. It's people!", "#20. Alton Brown's cakes don't rise. They ascend.", "#21. Some meats are so tender, they seem to melt in your mouth. Alton Brown's meats are so tender, he's had entire turkeys vanish into thin air.", "#22. Alton Brown's no saint. But if his chicken Kiev cures one more kid's leprosy, the church will reconsider the evidence.", "#23. Alton Brown doesn't whip potatoes. Alton Brown's potatoes whip themselves, if they know what's good for them.", "#24. Alton Brown's other car is the Wienermobile.", "#25. Alton Brown's show is called 'Good Eats', because 'Multiple Shuddering Mouthgasms' didn't play with the network's target demographic.", "#26. Alton Brown's freezer operates at minus-twenty-seven degrees. Kelvin.", "#27. Alton Brown once prepared shrimp gumbo for a cooking competition, using only salt, water, canned Spam, and a packet of Arby's 'Horsey Sauce'. He took second place. He would have won, but one of the judges was allergic to shellfish.", "#28. Alton Brown can fit three hundred and forty-two cookies on a standard-sized baking sheet. Without any touching.", "#29. When Alton Brown slices onions, the onions cry.", "#30. Alton Brown was once asked to participate in a blind orange juice taste test. He was the only person able to successfully identify the brand, style, vintage, temperature, pH level, distance to the orchard, age of the grove trees, and the names of the workers picking the fruit. Including the one who needs to start washing after bathroom breaks.", "#31. Your grandmother may make biscuits that taste light and airy. Alton Brown's biscuits have to be tethered, or they float right up the chimney.", "#32. Too many cooks spoil the soup. Unless one of those cooks is named Alton Brown.", "#33. Alton Brown ran a lemonade stand as a child, just like the rest of us. But Alton Brown's lemonade was so delicious, he bought his house with the profits.", "#34. Some salsas are so thick, a tortilla chip may break off when dipping. Alton Brown's salsa has been known to trap entire herds of wild deer.", "#35. Alton Brown grows truffles in his back yard. And at harvest time, he sniffs them out himself.", "#36. In Alton Brown's fridge, the open boxes of baking soda aren't thrown out when they're through absorbing odors. They go straight to the Louvre.", "#37. Like any trained chef, Alton Brown can make any of the five 'mother sauces'. But Alton Brown also makes father sauce, grandmother sauce, and great-uncle-twice-removed sauce.", "#38. Alton Brown's oven is a Hotternell.", "#39. Legend has it that a school of piranha can strip the meat from a full-grown cow in sixty seconds. Alton Brown can do it in thirty -- and wrap the cuts in butcher's paper, to boot.", "#40. Alton Brown's fudge brownies aren't simply dark and rich. Alton Brown's fudge brownies actually exert a mild gravitational pull.", "#41. Gordon Ramsay calls Alton Brown 'sir'.", "#42. Alton Brown was once pulled over by a traffic cop who asked to see his driver's license. Though he had forgotten his wallet, Alton Brown proved his identity on the spot by preparing a delicious stromboli using only the beef jerky, ketchup packets and stale doughnut scraps found in the officer's car. Needless to say, Alton Brown was not given a ticket that day.", "#43. To most people, 'a pinch of salt' is an approximate measure. To Alton Brown, a pinch of salt equals three hundred and twenty-four grains, exactly. And he can grab them, even blindfolded, every time.", "#44. Alton Brown doesn't need to brush. Alton Brown's teeth are coated with Teflon.", "#45. Cervantes famously said: 'Hunger is the best sauce in the world'. Cervantes clearly never tasted Alton Brown's remoulade.", "#46. Alton Brown doesn't use deodorant. Alton Brown brushes down with olive oil.", "#47. Some chefs can sculpt fancy swans out of foil to hold their diners' leftovers. Alton Brown's diners never have leftovers.", "#48. Alton Brown scrambles eggs into their individual component atoms. And can still make them into a tasty omelet.", "#49. Most souffles collapse if you breathe too loudly near them. Alton Brown's souffles are guaranteed fall-proof, up to 8.6 on the Richter scale.", "#50. Alton Brown's kitchen timer is an atomic clock. It's set to GMT (Gumsmacking Morsel Time).", "#51. You or I might cream leeks until they're tender. Alton Brown creams leeks until they say they're sorry.", "#52. Alton Brown once carved a rose garnish from a radish peel so lifelike, neighborhood bees tried to pollinate it. He planted and watered it, and now Alton Brown has a whole rose garnish garden in his back yard.", "#53. Some desserts are so tasty, they come with extra spoons. Alton Brown's desserts are so decadent, he cannot legally serve them without defibrillator paddles for every person within a three-mile radius.", "#54. Alton Brown owns the fastest mixer in existence. When he runs it in reverse, time flows backwards.", "#55. Alton Brown's egg slicer can cut through cue balls, too. And when he's done seasoning them, diners can't tell the difference.", "#56. Most chefs are happy when they've beaten egg whites into 'stiff peaks'. Alton Brown isn't satisfied until his egg whites can support a watermelon.", "#57. Alton Brown doesn't bother buying elbow macaroni. Alton Brown buys mezzani, and bends it with his will alone.", "#58. The sweat from Alton Brown's brow registers 30,000 units on the Scoville scale.", "#59. Alton Brown once attended a charity ball where a prize was awarded for the best donation. Though he showed up seemingly empty-handed, he won the prize, anyway. Because Alton Brown brought flavor to the party."]
	return {'text': random.choice(facts)}
command_aliases['altonbrown'] = 'altonbrownfact'
command_aliases['altonbrownfacts'] = 'altonbrownfact'

@bot_command(category="Random")
async def fn_shuffle(arg, p):
	choices = arg.split('/')
	random.shuffle(choices)
	return {'text': '/'.join(choices)}

@bot_command(category="Random")
async def fn_dice(arg, p):
	param = arg.split(' ')
	if len(param) != 2:
		return {'text': 'Syntax: dice num_dice num_sides'}
	else:
		dice = int(param[0])
		sides = int(param[1])
		sum = 0
		if dice < 1 or dice > 1000:
			return {'text': 'bad number of dice'}
		if sides < 1 or sides > 1000000000:
			return {'text': 'bad number of sides'}
		for i in range(dice):
			sum += random.randint(1, sides)
		return {'text': '%dd%d = %d' % (dice, sides, sum)}

@bot_command(hidden=True)
async def fn_my_ip(arg, p):
	return {'text': 'Running from %s' % subprocess.Popen('hostname -I', shell=True, stdout=subprocess.PIPE).stdout.read().decode()}

@bot_command()
async def fn_test(arg, p):
	return {'text': 'Hello!'}

@bot_command(category="Text")
async def fn_chr(arg, p):
	result = ''
	for x in arg.split(' '):
		result += chr(int(x))
	return {'text': result}

@bot_command(category="Text")
async def fn_chrx(arg, p):
	result = ''
	for x in arg.split(' '):
		result += chr(int(x, 16))
	return {'text': result}

@bot_command(category="Text")
async def fn_ord(arg, p):
	result = ''
	for c in arg:
		result += str(ord(c))+" "
	return {'text': result}

@bot_command(category="Text")
async def fn_ordx(arg, p):
	result = ''
	for c in arg:
		result += '%x ' % ord(c)
	return {'text': result}

@bot_command(category="Time")
async def fn_datediff(arg, p):
	two_dates = arg.split(' ')
	if len(two_dates) != 2:
		return {'text': 'Provide two dates to get a difference of, in M/D/Y format, or "now" for the current day'}
	d1 = date_from_string(two_dates[0])
	d2 = date_from_string(two_dates[1])
	difference = abs((d2 - d1).days)
	return {'text': '%d days (%d weeks %d days)' % (difference, difference/7, difference%7)}

@bot_command(category="Time")
async def fn_dateplus(arg, p):
	split = arg.split(' ')
	if len(split) != 2:
		return {'text': 'Provide a date in M/D/Y format and a number of days to add'}
	the_date = date_from_string(split[0]) + timedelta(days=int(split[1]))
	return {'text': the_date.strftime("%m/%d/%Y is a %A")}

@bot_command(category="Time")
async def fn_dayofweek(arg, p):
	the_date = date_from_string(arg)
	return {'text': the_date.strftime("%m/%d/%Y is a %A")}

@bot_command(category="Time")
async def fn_curtime(arg, p):
	return {'text': datetime.today().strftime("Now it's %m/%d/%Y, %I:%M %p")}

@bot_command(category="Random")
async def fn_boggle(arg, p):
	dice = ['ARELSC','TABIYL','EDNSWO','BIOFXR', 'MCDPAE','IHFYEE','KTDNUO','MOQAJB',
			'ESLUPT','INVTGE','ZNDVAE','UKGELY', 'OCATAI','ULGWIR','SPHEIN','MSHARO']
	random.shuffle(dice)

	out = ''
	for i in range(len(dice)):
		out += '%s ' % random.choice(dice[i])
		if (i % 4 == 3) and i != 15:
			out += '\n'

	return monospace(out)

#@bot_command
#async def fn_whoami(arg, p):
#	return {'text': 'You\'re %s (%s)' % (p['display_name'], p['username'])}

@bot_command(category="Text")
async def fn_strlen(arg, p):
	return {'text': str(len(arg))}

@bot_command(category="Text")
async def fn_strlenb(arg, p):
	return {'text': str(len(arg.encode('utf-8')))}

@bot_command(category="Emoji", alias=['emojiname', 'uniname'])
async def fn_unicode_name(arg, p):
	if not len(arg):
		return None
	def replace_name(emoji):
		if emoji == '⚧':
			return '**trans rights**'
		else:
			return unicode_name(emoji, 'Not found')
	return {'text': ', '.join(replace_name(x).capitalize() for x in arg[:10])}

@bot_command(category="Emoji", alias=['emoji'])
async def fn_random_emoji(arg, p):
	return {'text': '%s %s %s' % random_emoji(8)}
command_aliases['emoji'] = 'random_emoji'

@bot_command(category="Emoji", alias=['emojis'])
async def fn_random_emojis(arg, p):
	count = 10
	if len(arg) and arg.isnumeric():
		count = int(arg)
	if count > 60:
		count = 60
	return {'text': ''.join(random_emoji(8)[0] for x in range(count))}

@bot_command(category="Emoji", alias=['emojireacts'])
async def fn_random_emoji_reacts(arg, p):
	for i in range(10):
		try:
			await p['discord_message'].add_reaction(random_emoji(8)[0])
		except:
			pass

@bot_command(category="Emoji")
async def fn_eggplant(arg, p):
	await p['discord_message'].add_reaction('🍆')
	return None

@bot_command(category="Emoji")
async def fn_vote(arg, p):
	await p['discord_message'].add_reaction('👍')
	await p['discord_message'].add_reaction('👎')
	return None

@bot_command(hidden=True)
async def fn_reply(arg, p):
	await p['discord_message'].reply('Test')
	return None

@bot_command(category="Random")
async def fn_fakeregionnames(arg, p):
	return {'text': generate_provinces(arg)}

@bot_command(category="Random")
async def fn_fakecitynames(arg, p):
	return {'text': generate_settlements(arg)}

@bot_command(category="Programming")
async def fn_gbaddr(arg, p):
	split = arg.split(':')
	if len(split) == 2:
		hex1 = int(split[0], 16)
		hex2 = int(split[1], 16)
		return {'text': '0x%x' % (hex1 * 0x4000 + hex2 - 0x4000)}
	else:
		hex = int(arg, 16)
		return {'text': '%x:%x' % (hex // 0x4000, 0x4000 + (hex % 0x4000))}
command_aliases['gabddr'] = 'gbaddr'
command_aliases['gbadr']  = 'gbaddr'
command_aliases['gbadrd'] = 'gbaddr'
command_aliases['gbdadr'] = 'gbaddr'

@bot_command(category="Programming")
async def fn_th(arg, p):
	""" converts pasted output from FRHED """
	out = ''
	i = 0
	while i < len(arg):
		c = arg[i]
		b = 0 # the byte
		if arg[i:i+4] == '<bh:' and arg[i+6:i+7] == '>':
			b = int(arg[i+4:i+6], 16)
			i += 7
		elif arg[i:i+2] == '\\<':
			b = ord('<')
			i += 2
		elif arg[i:i+2] == '\\\\':
			b = ord('\\')
			i += 2
		else:
			b = ord(c)
			i += 1
		out += '%.2x ' % b
	return {'text': out}

@bot_command(category="Programming")
async def fn_z80asm(arg, p):
	if arg.find('incbin') >= 0 or arg.find('include') >= 0:
		return {'text': 'nice try'}
	else:
		remove_file('code.bin')
		file = open(temp_file('code.z80'), 'w') 
		file.write(arg)
		file.close()
		os.system('z80asm -o '+temp_file('code.bin')+' -i '+temp_file('code.z80'))
		return monospace(bytes_from_file('code.bin'))

@bot_command(category="Programming")
async def fn_ca65(arg, p):
	no_thanks = [".incbin", ".include", ".res", ".repeat"]
	lowercase = arg.lower()
	for bad in no_thanks:
		if lowercase.find(bad) >= 0:
			return {'text': '"'+bad+'" not allowed'}
	remove_file('code.bin')
	file = open(temp_file('code.asm'), 'w') 
	file.write(arg)
	file.close()
	if(os.system('/home/pi/code/cc65-2.19/bin/ca65 -o '+temp_file('code.o')+' -i '+temp_file('code.asm'))):
		return {'text': "Couldn't assemble"}
	if(os.system('/home/pi/code/cc65-2.19/bin/ld65 -o '+temp_file('code.bin')+' -C '+temp_file('6502.x')+' '+temp_file('code.o'))):
		return {'text': "Couldn't link"}
	return monospace(bytes_from_file('code.bin'))

@bot_command(category="Programming")
async def fn_da65(arg, p):
	split = [int(s,16) for s in arg.split(' ')]
	file = open(temp_file('code.bin'), 'wb') 
	file.write(bytearray(split))
	file.close()
	out = subprocess.Popen('/home/pi/code/cc65-2.19/bin/da65 '+temp_file('code.bin')+' --mnemonic-column 1 --argument-column 10 --comments 0', shell=True, stdout=subprocess.PIPE).stdout.read().decode()

	# trim the stuff on the top off
	setcpu = out.find('.setcpu')
	if setcpu >= 0:
		out = out[setcpu:]
		# trim the .setcpu off
		lines = out.split('\n')
		out = '\n'.join(lines[2:])
	return monospace(out)

@bot_command()
async def fn_nesgenie(arg, p):
	if len(arg) == 0:
		return {'text': 'Please give one of the following:\n6 or 8 character Game Genie code\nAAAA DD, where A=address, D=data (in hex)\nAAAA DD CC, where A=address, D=data C=compare\n'}
	arg = arg.upper()
	key = 'APZLGITYEOXUKSVN'

	split = arg.split(' ')
	if len(split) == 1:   # decode
		for c in arg:
			if key.find(c) == -1:
				return {'text': '"%s" is an invalid NES Game Genie character, use APZLGITYEOXUKSVN' % c}
		if len(arg) != 6 and len(arg) != 8:
			return {'text': 'NES Game Genie codes must be 6 or 8 characters long'}

		# start decoding
		n = []
		for c in arg:
			n.append(key.find(c))
		address = 0x8000 + (((n[3] & 7) << 12) | ((n[5] & 7) << 8) | ((n[4] & 8) << 8) \
			| ((n[2] & 7) << 4) | ((n[1] & 8) << 4) | (n[4] & 7) | (n[3] & 8));

		if len(arg) == 6:
			data = ((n[1] & 7) << 4) | ((n[0] & 8) << 4) | (n[0] & 7) | (n[5] & 8);
			return {'text': '%s is %.4X %.2x' % (arg, address, data)}
		else:
			data = ((n[1] & 7) << 4) | ((n[0] & 8) << 4) | (n[0] & 7) | (n[7] & 8);
			compare = ((n[7] & 7) << 4) | ((n[6] & 8) << 4) | (n[6] & 7) | (n[5] & 8);
			return {'text': '%s is %.4X %.2X (compare %.2X)' % (arg, address, data, compare)}
	elif len(split) == 2: # encode without compare
		addr   = int(split[0],16)
		data   = int(split[1],16)
		output = ''
		output += key[(data>>4 & 8) | (data & 7)];
		output += key[(addr>>4 & 8) | (data>>4 & 7)];
		output += key[0 | (addr>>4 & 7)];
		output += key[(addr & 8) | (addr>>12 & 7)];
		output += key[(addr>>8 & 8) | (addr & 7)];
		output += key[(data & 8) | (addr>>8 & 7)];
		return {'text': '%.4X %.2X = %s' % (addr, data, output)}
	elif len(split) == 3: # encode with compare
		addr    = int(split[0],16)
		data    = int(split[1],16)
		compare = int(split[2],16)
		output = ''
		output += key[(data>>4 & 8) | (data & 7)];
		output += key[(addr>>4 & 8) | (data>>4 & 7)];
		output += key[8 | (addr>>4 & 7)];
		output += key[(addr & 8) | (addr>>12 & 7)];
		output += key[(addr>>8 & 8) | (addr & 7)];
		output += key[(compare & 8) | (addr>>8 & 7)];
		output += key[(compare>>4 & 8) | (compare & 7)];
		output += key[(data & 8) | (compare>>4 & 7)];
		return {'text': '%.4X %.2X %.2X = %s' % (addr, data, compare, output)}
	return {'text': 'test'}

async def join_voice_with_user(user):
	if user != None and user.voice != None and user.voice.channel != None:
		guild = user.guild.id
		if guild in voice_clients:
			await leave_voice(user)
		voice_clients[guild] = await user.voice.channel.connect()

async def leave_voice(user):
	guild = user.guild.id
	if guild in voice_clients:
		await voice_clients[guild].disconnect()
		del voice_clients[guild]

@bot_command(category="Voice")
async def fn_joinvoice(arg, p):
	await join_voice_with_user(p['discord_message'].author)
	return None

@bot_command(category="Voice")
async def fn_leavevoice(arg, p):
	await leave_voice(p['discord_message'].author)
	return None

@bot_command(category="Voice")
async def fn_pause(arg, p):
	guild = p['discord_message'].guild.id
	if guild in voice_clients:
		voice_clients[guild].pause()
	return None

@bot_command(category="Voice")
async def fn_stop(arg, p):
	guild = p['discord_message'].guild.id
	if guild in voice_clients:
		voice_clients[guild].stop()
	return None

@bot_command(category="Voice")
async def fn_resume(arg, p):
	guild = p['discord_message'].guild.id
	if guild in voice_clients:
		voice_clients[guild].resume()
	return None

async def play_ffmpeg_audio(user, music):
	guild = user.guild.id
	not_in_channel_already = guild not in voice_clients
	if guild not in voice_clients:
		await join_voice_with_user(user)
	if guild in voice_clients:
		if voice_clients[guild].is_playing():
			voice_clients[guild].stop()
		voice_clients[guild].play(discord.FFmpegPCMAudio(executable=ffmpeg_path, source=music))
		if not_in_channel_already:
			while guild in voice_clients and voice_clients[guild].is_playing():
				await asyncio.sleep(.1)
			await leave_voice(user)
		return None
	return {'text': 'Join a voice channel before using that command!'}

@bot_command(category="Voice")
async def fn_barrelroll(arg, p):
	return await play_ffmpeg_audio(p['discord_message'].author, "mp3/doabarrelroll.mp3")

@bot_command(category="Voice")
async def fn_cory(arg, p):
	return await play_ffmpeg_audio(p['discord_message'].author, "mp3/cory.mp3")

@bot_command(category="Voice")
async def fn_play(arg, p):
	if arg.isalnum():
		return await play_ffmpeg_audio(p['discord_message'].author, "mp3/%s.mp3" % arg)

@bot_command()
async def fn_allcommands(arg, p):
	return {'text': '\n'.join(
		['**%s**: %s' % (category, ', '.join(list(command_categories[category]))) for category in command_categories]
	)}

@bot_command()
async def fn_help(arg, p):
	return {'text': 'Take a look at https://t.novasquirrel.com/cathy.html'}

@bot_command()
async def fn_foresee(arg, p):
	return {'text': 'https://i.ytimg.com/vi/-8gVcI0VAbc/maxresdefault.jpg'}

@bot_command(category="Random")
async def fn_would(arg, p):
	return {'text': 'I would %s %s %s' % (random.choice(many_verbs), random.choice(["his", "her", "their", "my", "the"]), random.choice(many_nouns))}

@bot_command(category="Random")
async def fn_lammy(arg, p):
	return {'text': 'Lammy would %s %s %s by playing it like a guitar' % (random.choice(many_verbs), random.choice(["his", "her", "their", "my", "the"]), random.choice(many_nouns))}

@bot_command(category="Random")
async def fn_myspecibus(arg, p):
	return {'text': 'My strife specibus is %skind' % random.choice(many_nouns)}

@bot_command()
async def fn_thou(arg, p):
	return {'text': 'Thou %s %s %s!' % (random.choice(["artless", "bawdy", "beslubbering", "bootless", "churlish", "cockered", "clouted", "craven", "currish", "dankish", "dissembling", "droning", "errant", "fawning", "fobbing", "froward", "frothy", "gleeking", "goatish", "gorbellied", "impertinent", "infectious", "jarring", "loggerheaded", "lumpish", "mammering", "mangled", "mewling", "paunchy", "pribbling", "puking", "puny", "qualling", "rank", "reeky", "roguish", "ruttish", "saucy", "spleeny", "spongy", "surly", "tottering", "unmuzzled", "vain", "venomed", "villainous", "warped", "wayward", "weedy", "yeasty"]), random.choice(["base-courted", "bat-fowling", "beef-witted", "beetle-headed", "boil-brained", "clapper-clawed", "clay-brained", "common-kissing", "crook-pated", "dismal-dreaming", "dizzy-eyed", "doghearted", "dread-bolted", "earth-vexing", "elf-skinned", "fat-kidneyed", "fen-sucked", "flap-mouthed", "fly-bitten", "folly-fallen", "fool-born", "full-gorged", "guts-griping", "half-faced", "hasty-witted", "hedge-born", "hell-hated", "idle-headed", "ill-breeding", "ill-nurtured", "knotty-pated", "milk-livered", "motley-minded", "onion-eyed", "plume-plucked", "pottle-deep", "pox-marked", "reeling-ripe", "rough-hen", "rude-growing", "rump-fed", "sheep-biting", "spur-galled", "swag-bellied", "tardy-gaited", "tickle-brained", "toad-spotted", "urchin-snouted", "weather-bitten"]), random.choice(["apple-john", "baggage", "barnacle", "bladder", "boar-pig", "bugbear", "bum-bailey", "canker-blossom", "clack-dick", "clotpole", "coxcomb", "codpiece", "death-token", "dewberry", "flap-dragon", "flax-wench", "flirt-gill", "foot-licker", "fustilarian", "giglet", "gudgeon", "haggard", "harpy", "hedge-pig", "horn-beast", "hugger-bugger", "joithead", "lewdster", "lout", "maggot-pie", "malt-worm", "mammet", "measle", "minnow", "miscreant", "moldwarp", "mumble-news", "nut-hook", "pigeon-egg", "pignut", "puttock", "pumpion", "ratsbane", "scut", "skainsmate", "strumpet", "varlot", "vassal", "wheyface", "wagtail"]))}

@bot_command(category="Emoji")
async def fn_guildemojis(arg, p):
	guild = p['discord_message'].guild
	return {'text': ' '.join([str(x) for x in guild.emojis])}

@bot_command(category="Emoji", hidden=True)
async def fn_guildemojinames(arg, p):
	guild = p['discord_message'].guild
	return {'text': ' '.join([x.name for x in guild.emojis])}

@bot_command(category="Emoji")
async def fn_guildemoji(arg, p):
	guild = p['discord_message'].guild
	for emoji in guild.emojis:
		if emoji.name == arg:
			return {'text': str(emoji)}
	else:
		return None

@bot_command(category="Emoji")
async def fn_clientemoji(arg, p):
	client = p['client']
	for emoji in client.emojis:
		if emoji.name == arg:
			return {'text': str(emoji)}
	else:
		return None

async def image_filter_on_message(message, filter):
	filenames = ["mario", "wario", "luigi", "waluigi", "hamtaro", "sans", "mariokart", "doritos", "fritos", "toast", "burgerking", "aldi", "lidl"]

	if len(message.attachments) == 0 and len(message.stickers) == 0:
		return {'text': 'I don\'t see an attachment on that message. Upload an image with that command as the text'}
	else:
		if len(message.attachments) != 0:
			bytes_in_attachment = await message.attachments[0].read()
		elif len(message.stickers) != 0:
			sticker = message.stickers[0].image_url
			if sticker:
				bytes_in_attachment = await sticker.read()			
		if bytes_in_attachment != None:
			try:
				opened_image = Image.open(io.BytesIO(bytes_in_attachment))
			except Exception:
				return {'text': 'Bad image?'}

			edited_image = await filter(opened_image)

			if isinstance(edited_image, tuple):
				f = discord.File(edited_image[0], filename=random.choice(filenames)+edited_image[1])
				await message.channel.send(file=f)
				edited_image[0].close()
				return None
			elif isinstance(edited_image, str):
				return {'text': edited_image}
			elif edited_image:
				edited_image_as_file = io.BytesIO()
				edited_image.save(edited_image_as_file, format='PNG')
				edited_image_as_file.seek(0,2) # Move to the end
				filesize = edited_image_as_file.tell()

				filesize_limit = 8388608
				if message.guild:
					filesize_limit = message.guild.filesize_limit
				if filesize >= filesize_limit:
					edited_image_as_file.close()
					edited_image.close()
					return {'text': 'Whoops, the resulting file from that was over 8MB'}
				edited_image_as_file.seek(0)

				f = discord.File(edited_image_as_file, filename=random.choice(filenames)+'.png')
				await message.channel.send(file=f)
				edited_image_as_file.close()
				edited_image.close()
				return None
			else:
				return {'text': 'Bad image or filter parameters?'}

async def image_filter_on_msg_or_reply(message, filter, commandname):
	async with message.channel.typing():
		if len(message.attachments) or len(message.stickers):
			return await image_filter_on_message(message, filter)
		if message.reference and message.reference.resolved:
			return await image_filter_on_message(message.reference.resolved, filter)
		return {'text': 'Upload an image (or reply to an image) with `%s` as the text' % commandname}

@bot_command(category="Image")
async def fn_hamtaro_eat(arg, p):
	async def hamtaro_edit(food):
		meme = Image.open('hamtaro.png')
		above = Image.open('hamtaro_above.png')
		food.thumbnail((95, 95))
		food2 = Image.new('RGBA', (meme.width, meme.height), (0, 0, 0, 0))
		food2.paste(food, (395-food.width//2, 260-food.height//2))
		meme.paste(food2, None, food2)
		meme.paste(above, None, above)
		above.close()
		food2.close()
		return meme
	return await image_filter_on_msg_or_reply(p['discord_message'], hamtaro_edit, 'ca.hamtaro_eat')

def parse_deepfry_colors(arg):
	split = [x for x in arg.replace('#','').split(' ') if len(x) == 6]
	if len(split) == 2 and len(split[0]) == 6 and len(split[1]) == 6:
		r1 = int(split[0][0:2], 16)
		g1 = int(split[0][2:4], 16)
		b1 = int(split[0][4:6], 16)
		r2 = int(split[1][0:2], 16)
		g2 = int(split[1][2:4], 16)
		b2 = int(split[1][4:6], 16)
		return ((r1, g1, b1,), (r2, g2, b2,))
	return ((254, 0, 2), (255, 255, 15))

def parse_color_list(arg, minimum_count=1):
	split = [x for x in arg.replace('#','').split(' ') if len(x) == 6]
	if len(split) >= minimum_count:
		out = []
		for color in split:
			r = int(color[0:2], 16)
			g = int(color[2:4], 16)
			b = int(color[4:6], 16)
			out.append((r,g,b,))
		out = tuple(out)
		return out
	return ((254, 0, 2), (255, 255, 15))

@bot_command(category="Image")
async def fn_colorize(arg, p):
	colors = parse_color_list(arg, minimum_count = 2)
	async def function(image):
		if len(colors) == 2:
			return ImageOps.colorize(ImageOps.grayscale(image).split()[0], colors[0], colors[1])
		if len(colors) >= 3:
			return ImageOps.colorize(ImageOps.grayscale(image).split()[0], colors[0], colors[2], mid=colors[1])
	return await image_filter_on_msg_or_reply(p['discord_message'], function, 'ca.colorize')

@bot_command(category="Image")
async def fn_solarize(arg, p):
	if(arg == ''):
		arg = 128
	async def function(image):
		return ImageOps.solarize(image.convert('RGB'), int(arg))
	return await image_filter_on_msg_or_reply(p['discord_message'], function, 'ca.solarize')

@bot_command(category="Image")
async def fn_posterize(arg, p):
	if(arg == ''):
		arg = 4
	async def function(image):
		amount = int(arg)
		if(amount > 8):
			amount = 8
		if(amount < 1):
			amount = 1
		return ImageOps.posterize(image.convert('RGB'), int(arg))
	return await image_filter_on_msg_or_reply(p['discord_message'], function, 'ca.posterize')

@bot_command(category="Image")
async def fn_grayscale(arg, p):
	async def function(image):
		return ImageOps.grayscale(image.convert('RGBA'))
	return await image_filter_on_msg_or_reply(p['discord_message'], function, 'ca.grayscale')

@bot_command(category="Image")
async def fn_vflip(arg, p):
	async def function(image):
		return ImageOps.flip(image)
	return await image_filter_on_msg_or_reply(p['discord_message'], function, 'ca.vflip')

@bot_command(category="Image")
async def fn_hflip(arg, p):
	async def function(image):
		return ImageOps.mirror(image)
	return await image_filter_on_msg_or_reply(p['discord_message'], function, 'ca.hflip')

@bot_command(category="Image")
async def fn_equalize(arg, p):
	async def function(image):
		return ImageOps.equalize(image.convert('RGBA'))
	return await image_filter_on_msg_or_reply(p['discord_message'], function, 'ca.equalize')

@bot_command(category="Image")
async def fn_invert(arg, p):
	async def function(image):
		return ImageOps.invert(image.convert('RGBA'))
	return await image_filter_on_msg_or_reply(p['discord_message'], function, 'ca.invert')

@bot_command(category="Image")
async def fn_autocrop(arg, p):
	async def function(image):
		return image.crop(image.getbbox())
	return await image_filter_on_msg_or_reply(p['discord_message'], function, 'ca.autocrop')

@bot_command(category="Image")
async def fn_deepfry(arg, p):
	colors = parse_deepfry_colors(arg)
	async def function(image):
		return await deepfry(image, colours = colors, flares = False)
	return await image_filter_on_msg_or_reply(p['discord_message'], function, 'ca.deepfry')

@bot_command(category="Image")
async def fn_deepfry_keepcolor(arg, p):
	colors = parse_deepfry_colors(arg)
	async def function(image):
		return await deepfry(image, colours = None, flares = False)
	return await image_filter_on_msg_or_reply(p['discord_message'], function, 'ca.deepfry_keepcolor')

@bot_command(category="Image")
async def fn_deepfry_flare(arg, p):
	colors = parse_deepfry_colors(arg)
	async def function(image):
		return await deepfry(image, colours = colors, flares = True)
	return await image_filter_on_msg_or_reply(p['discord_message'], function, 'ca.deepfry_flare')

@bot_command(category="Image")
async def fn_thumbnail(arg, p):
	split = arg.split(' ')
	if len(split) < 2:
		return {'text': 'You need to provide a width and a height'}
	width = min(2048, int(split[0]))
	height = min(2048, int(split[1]))

	async def function(image):
		image.thumbnail((width, height))
		return image
	return await image_filter_on_msg_or_reply(p['discord_message'], function, 'ca.thumbnail width height')

@bot_command(category="Image")
async def fn_resize(arg, p):
	split = arg.lower().split(' ')
	if len(split) < 2:
		return {'text': 'You need to provide a width and a height'}
	width = min(2048, int(split[0]))
	height = min(2048, int(split[1]))
	resample = Image.BICUBIC
	if len(split) >= 3:
		if split[2] == 'nearest':
			resample = Image.NEAREST
		elif split[2] == 'box':
			resample = Image.BOX
		elif split[2] == 'linear' or split[2] == 'bilinear':
			resample = Image.BILINEAR
		elif split[2] == 'hamming':
			resample = Image.HAMMING
		elif split[2] == 'cubic' or split[2] == 'bicubic':
			resample = Image.BICUBIC
		elif split[2] == 'lanczos':
			resample = Image.LANCZOS

	async def function(image):
		return image.resize((width, height), resample=Image.NEAREST if image.mode == 'P' else resample)
	return await image_filter_on_msg_or_reply(p['discord_message'], function, 'ca.resize width height')

@bot_command(category="Image")
async def fn_rotate(arg, p):
	split = arg.lower().split(' ')
	if arg == '':
		return {'text': 'You need to provide a width and a height'}
	angle = float(split[0])
	resample = Image.BICUBIC
	if len(split) >= 2:
		if split[1] == 'nearest':
			resample = Image.NEAREST
		elif split[1] == 'linear' or split[1] == 'bilinear':
			resample = Image.BILINEAR
		elif split[1] == 'cubic' or split[1] == 'bicubic':
			resample = Image.BICUBIC

	async def function(image):
		return image.rotate(angle, expand=True, resample=Image.NEAREST if image.mode == 'P' else resample)
	return await image_filter_on_msg_or_reply(p['discord_message'], function, 'ca.rotate angle')

hand = Image.open('hand.png')
@bot_command(category="Image")
async def fn_petgif(arg, p):
	# Derived from https://benisland.neocities.org/petpet/main.js
	OUT_SIZE = 112
	g = {
	  'squish': 1.25,
	  'scale': 0.875,
	  'delay': 60,
	  'spriteX': 14,
	  'spriteY': 20,
	  'spriteWidth': 112,
	  'spriteHeight': 112,
	  'currentFrame': 0,
	}
	frameOffsets = [
		{ 'x': 0, 'y': 0, 'w': 0, 'h': 0 },
		{ 'x': -4, 'y': 12, 'w': 4, 'h': -12 },
		{ 'x': -12, 'y': 18, 'w': 12, 'h': -18 },
		{ 'x': -8, 'y': 12, 'w': 4, 'h': -12 },
		{ 'x': -4, 'y': 0, 'w': 0, 'h': 0 },
	]
	async def function(sprite):
		def renderFrame(frame):
			im = Image.new('RGBA', (OUT_SIZE, OUT_SIZE), (0, 0, 0, 0))

			offset = frameOffsets[frame]
			dx = int(g['spriteX'] + offset['x'] * (g['squish'] * 0.4))
			dy = int(g['spriteY'] + offset['y'] * (g['squish'] * 0.9))
			dw = int((g['spriteWidth'] + offset['w'] * g['squish']) * g['scale'])
			dh = int((g['spriteHeight'] + offset['h'] * g['squish']) * g['scale'])

			im.paste(sprite.resize((dw, dh)), (dx, dy))

			padded_hand = hand.crop((frame * OUT_SIZE, 0, frame * OUT_SIZE + OUT_SIZE, OUT_SIZE))
			padded_hand = padImage(padded_hand, 0, max(0, int(dy * 0.75 - max(0, g['spriteY']) - 0.5)), OUT_SIZE, OUT_SIZE)

			im.paste(padded_hand, None, padded_hand)
			return im
		frames = [renderFrame(x) for x in range(5)]

		as_file = io.BytesIO()
		save_transparent_gif(frames, 60, as_file)
		as_file.seek(0)
		return (as_file, '.gif')
	return await image_filter_on_msg_or_reply(p['discord_message'], function, 'ca.petgif')

@bot_command(category="Image")
async def fn_spingif(arg, p):
	duration = 60
	if arg != '':
		duration = int(arg)

	async def function(sprite):
		width = 256
		height = 256
		sprite.thumbnail((width, height))
		sprite = padImage(sprite, int(width/2-sprite.width/2), int(height/2-sprite.height/2), width, height)
		frames = [sprite.rotate(360/32*i) for i in range(32)]

		as_file = io.BytesIO()
		save_transparent_gif(frames, duration, as_file)
		as_file.seek(0)
		return (as_file, '.gif')
	return await image_filter_on_msg_or_reply(p['discord_message'], function, 'ca.spingif')

@bot_command(category="Image")
async def fn_jpegify(arg, p):
	the_quality = False
	times = 10
	def reduce_quality(i, quality, final):
		as_file = io.BytesIO()
		if quality == False: # Random quality
			quality = random.randint(1, 95)
		i.save(as_file, format='JPEG', quality=quality)
		as_file.seek(0)
		if final:
			return (as_file, '.jpg')
		reread = Image.open(as_file)
		reread.load()
		as_file.close()
		return reread

	if len(arg):
		split = arg.split(' ')
		if len(split) >= 1:
			if split[0] == '?':
				the_quality = False
			else:
				the_quality = int(split[0])
				times = 1
		if len(split) >= 2:
			times = min(100, max(1, int(split[1])))
	
	async def function(image):
		image = image.convert('RGB')
		if times > 1:
			for i in range(times-1):
				image = reduce_quality(image, the_quality, False)
		return reduce_quality(image, the_quality, True)
	return await image_filter_on_msg_or_reply(p['discord_message'], function, 'ca.jpegify')

class Event_ts(asyncio.Event):
    #TODO: clear() method
    def set(self):
        #FIXME: The _loop attribute is not documented as public api!
        self._loop.call_soon_threadsafe(super().set)

def rotpixels_thread(event, image, out, angle, scale, inpar, outpar, outsize, subevents):
	out[0] = rotpixels(image, angle=angle, scale=scale, inpar=inpar, outpar=outpar, outsize=outsize, events=subevents)
	event.set()

@bot_command(category="Image")
async def fn_rotpixels(arg, p):
	angle = 0.0
	scale = 1.0
	in_par = 1.0
	out_par = 1.0

	out_width = None
	out_height = None
	autopad = False
	to_rgb = False
	to_rgba = True
	crop = False

	if arg == '':
		return None
	args = arg.split(' ')
	if len(args) >= 1:
		angle = float(args[0])
	if len(args) >= 2:
		scale = float(args[1])
	other_args = args[2:]
	for idx, val in enumerate(other_args):
		if val == 'inpar':
			in_par = float(other_args[idx+1])
		elif val == 'outpar':
			out_par = float(other_args[idx+1])
		elif val == 'autopad':
			autopad = True
		elif val == 'paletted':
			to_rgba = False
		elif val == 'rgb':
			to_rgb = True
		elif val == 'outsize':
			out_width = int(other_args[idx+1])
			out_height = int(other_args[idx+2])
		elif val == 'outwidth':
			out_width = int(other_args[idx+1])
		elif val == 'outheight':
			out_height = int(other_args[idx+1])
		elif val == 'crop':
			crop = True
	if scale > 8.0:
		scale = 8.0
	if scale <= 0:
		scale = 1.0

	async def function(image):
		if image.width > 512 or image.height > 512:
			return "Image too big, keep it under 512x512?"
		if image.width * scale > 512 or image.height * scale > 512:
			return "Image scaled too big, keep it under 512x512?"
		if to_rgb:
			image = image.convert('RGB')
		elif to_rgba:
			image = image.convert('RGBA')
		size = None
		if out_width and out_height:
			size = (out_width, out_height)
		elif out_width and out_height == None:
			size = (out_width, image.height)
		elif out_width == None and out_height:
			size = (image.width, out_height)
		if (out_width and out_width > 512) or (out_height and out_height > 512):
			return "Image output size too big, keep it under 512x512?"
		if autopad:
			m = max(image.width, image.height)
			size = (m, m)

		import threading
		e = Event_ts()
		sub_events = [Event_ts(), Event_ts(), Event_ts(), Event_ts()]
		out = [None]
		thread = threading.Thread(target=rotpixels_thread, args=(e, image, out, angle, scale, in_par, out_par, size, sub_events))
		thread.start()

		progress = await p['discord_message'].channel.send('Rotpixels (1/5): scale2x')
		await sub_events[0].wait()
		if progress:
			await progress.edit(content="Rotpixels (2/5): rotate")
		await sub_events[1].wait()
		if progress:
			await progress.edit(content="Rotpixels (3/5): mode filter")
		await sub_events[2].wait()
		if progress:
			await progress.edit(content="Rotpixels (4/5): find fewest edges")
		await sub_events[3].wait()
		if progress:
			await progress.edit(content="Rotpixels (5/5): resizing")
		await e.wait()
		if progress:
			await progress.delete()
		if crop:
			out[0] = out[0].crop(out[0].getbbox())
		return out[0]
	return await image_filter_on_msg_or_reply(p['discord_message'], function, 'ca.rotpixels angles scale')

@bot_command(category="Image")
async def fn_unicorn(arg, p):
	if arg == '':
		arg = str(p['discord_message'].author.id)

	hashed = hashlib.md5(arg.encode('utf-8')).hexdigest()

	as_file = io.BytesIO()
	as_file.write(create_avatar(128, int(hashed, 16)))
	as_file.seek(0)
	reread = Image.open(as_file)
	reread.load()
	as_file.close()

	as_png = io.BytesIO()
	reread.save(as_png, format='PNG')
	as_png.seek(0)

	f = discord.File(as_png, filename='unicorn.png')
	await p['discord_message'].channel.send(file=f)

	as_png.close()
	return None

@bot_command(category="Image")
async def fn_random_islands(arg, p):
	if arg == '':
		arg = 75.0
	image = random_islands(float(arg))
	#if image == None:
	#	return {'text': 'Error parsing that argument list'}

	as_png = io.BytesIO()
	image.save(as_png, format='PNG')
	as_png.seek(0)

	f = discord.File(as_png, filename='islands.png')
	await p['discord_message'].channel.send(file=f)

	as_png.close()
	return None
command_aliases['randomislands'] = 'random_islands'

@bot_command(category="Emoji")
async def fn_sheriff(arg, p):
	message = ".\n"+"⠀ ⠀ ⠀ :cowboy:\n"+"　 %s%s%s\n"+"%s     %s　%s\n"+":point_down: %s%s  :point_down:\n"+"　 %s　%s\n"+"　 %s　 %s\n"+"　 :boot:       :boot:\nHowdy I'm the sheriff of %s"
	if len(arg) == 0:
		arg = random_emoji(8)[0]
	return {"text": message % (arg, arg, arg,arg, arg, arg, arg, arg, arg, arg, arg, arg, arg)}
command_aliases['sherriff'] = 'sheriff'
command_aliases['sherrif'] = 'sheriff'

@bot_command(category="Image")
async def fn_blur(arg, p):
	async def function(image):
		return image.convert('RGBA').filter(ImageFilter.BLUR)
	return await image_filter_on_msg_or_reply(p['discord_message'], function, 'ca.blur')

@bot_command(category="Image")
async def fn_contour(arg, p):
	async def function(image):
		return image.convert('RGBA').filter(ImageFilter.CONTOUR)
	return await image_filter_on_msg_or_reply(p['discord_message'], function, 'ca.contour')

@bot_command(category="Image")
async def fn_detail(arg, p):
	async def function(image):
		return image.convert('RGBA').filter(ImageFilter.DETAIL)
	return await image_filter_on_msg_or_reply(p['discord_message'], function, 'ca.detail')

@bot_command(category="Image")
async def fn_edge_enhance(arg, p):
	async def function(image):
		return image.convert('RGBA').filter(ImageFilter.EDGE_ENHANCE)
	return await image_filter_on_msg_or_reply(p['discord_message'], function, 'ca.edge_enhance')
command_aliases['edgeenhance'] = 'edge_enhance'

@bot_command(category="Image")
async def fn_emboss(arg, p):
	async def function(image):
		return image.convert('RGBA').filter(ImageFilter.EMBOSS)
	return await image_filter_on_msg_or_reply(p['discord_message'], function, 'ca.emboss')

@bot_command(category="Image")
async def fn_find_edges(arg, p):
	async def function(image):
		return image.convert('RGB').filter(ImageFilter.FIND_EDGES)
	return await image_filter_on_msg_or_reply(p['discord_message'], function, 'ca.find_edges')
command_aliases['findedges'] = 'find_edges'

@bot_command(category="Image")
async def fn_sharpen(arg, p):
	async def function(image):
		return image.convert('RGBA').filter(ImageFilter.SHARPEN)
	return await image_filter_on_msg_or_reply(p['discord_message'], function, 'ca.sharpen')

@bot_command(category="Image")
async def fn_smooth(arg, p):
	async def function(image):
		return image.convert('RGBA').filter(ImageFilter.SMOOTH)
	return await image_filter_on_msg_or_reply(p['discord_message'], function, 'ca.smooth')

@bot_command(category="Image")
async def fn_smooth_more(arg, p):
	async def function(image):
		return image.convert('RGBA').filter(ImageFilter.SMOOTH_MORE)
	return await image_filter_on_msg_or_reply(p['discord_message'], function, 'ca.smooth_more')
command_aliases['smoothmore'] = 'smooth_more'

def color_cuber_thread(event, image, out, iterations):
	out[0] = color_cuber(image, iterations)
	event.set()

@bot_command(category="Image")
async def fn_color_cuber(arg, p):
	iterations = 400
	if arg != '':
		iterations = int(arg)
	if iterations < 1:
		iterations = 1
	if iterations > 1024:
		iterations = 1024
	async def function(image):
		import threading
		e = Event_ts()
		out = [None]
		thread = threading.Thread(target=color_cuber_thread, args=(e, image, out, iterations))
		thread.start()
		await e.wait()
		return out[0]
	return await image_filter_on_msg_or_reply(p['discord_message'], function, 'ca.color_cuber')
command_aliases['colorcuber'] = 'color_cuber'
command_aliases['colorcube'] = 'color_cuber'
command_aliases['colorcubes'] = 'color_cuber'

@bot_command(category="Image")
async def fn_filter(arg, p):
	filters = {
		"blur": ImageFilter.BLUR,
		"contour": ImageFilter.CONTOUR,
		"detail": ImageFilter.DETAIL,
		"edge_enhance": ImageFilter.EDGE_ENHANCE,
		"edge_enhance_more": ImageFilter.EDGE_ENHANCE_MORE,
		"emboss": ImageFilter.EMBOSS,
		"find_edges": ImageFilter.FIND_EDGES,
		"sharpen": ImageFilter.SHARPEN,
		"smooth": ImageFilter.SMOOTH,
		"smooth_more": ImageFilter.SMOOTH_MORE,
	}
	arg = arg.lower()
	if arg in filters:
		which = filters[arg]
	else:
		return {'text': 'ca.filter filtername, where filtername is one of ' + ', '.join(filters.keys())}

	async def function(image):
		return image.filter(which)
	return await image_filter_on_msg_or_reply(p['discord_message'], function, 'ca.filter')

@bot_command(category="Random")
async def fn_cricecorn(arg, p):
	subspecies = random.choice(["special", "spicecorn", "skycecorn", "cricecorn", "candycorn", "cricecorn", "skycecorn", "icecorn", "spicecorn", "cricecorn", "cricecorn", "candycorn", "spicecorn", "icecorn", "skycecorn", "cricecorn", "candycorn", "icecorn", "cricecorn", "special"])

	if subspecies == 'special':
		subspecies = random.choice(["angel cricecorn", "thundercloud cricecorn", "fairy cricecorn", "crystal cricecorn", "aquatic cricecorn", "devil cricecorn"])

	furcolor = random.choice(["natural fur color", "fur color of burning love", "natural fur color", "natural (dark) fur color", "a moody fur color", "fur color of a clear sky", "natural (light) fur color", "fur color of a forest", "natural fur color", "fur color of sweet love", "natural (light) fur color", "fur color of new leaves", "fur color of a clear sky", "natural (dark) fur color", "fur color of a deep sea", "natural fur color", "natural (light) fur color", "fur color of angel wings", "natural (dark) fur color"])
	furpattern = random.choice(["normal pattern", "banded pattern", "piebald pattern", "dappled pattern", "spotted pattern", "any pattern you like"])

	mutation = random.choice(["hairless", "floppy ears", "extra horn", "long hair", "long tail", "traits of another animal", "magic user", "curved horn", "glowing eyes/horn", "traits of a plant"])

	return {'text': 'A%s %s with %s, in %s. Optional mutation: %s' % ('n' if (subspecies[0] == 'a' or subspecies[0]=='i') else '', subspecies, furcolor, furpattern, mutation)}

@bot_command(category="Web API")
async def fn_agify(arg, p):
	if arg == '':
		return {'text': 'Please supply a name to check'}
	arg = arg.split(' ')
	params = {'name': arg[0]}
	if len(arg) > 1 and len(arg[1]) == 2:
		params['country_id'] = arg[1]
	async with aiohttp.ClientSession() as session:
		url = 'https://api.agify.io'
		async with session.get(url, params=params) as resp:
			data = await resp.json()
			if data['age']:
				return {'text' : 'Agify thinks the name \"%s\" sounds %d years old (count %d)' % (data['name'], data['age'], data['count'])}
			else:
				return {'text' : 'Agify doesn\'t know how old that name sounds'}

@bot_command(category="Web API")
async def fn_genderize(arg, p):
	if arg == '':
		return {'text': 'Please supply a name to check'}
	arg = arg.split(' ')
	params = {'name': arg[0]}
	if len(arg) > 1 and len(arg[1]) == 2:
		params['country_id'] = arg[1]
	async with aiohttp.ClientSession() as session:
		url = 'https://api.genderize.io/'
		async with session.get(url, params=params) as resp:
			data = await resp.json()
			if data['gender']:
				return {'text' : 'Genderize thinks the name \"%s\" sounds %s (probability %s, count %d)' % (data['name'], data['gender'], data['probability'], data['count'])}
			else:
				return {'text' : 'Genderize doesn\'t what gender that name is'}

@bot_command(category="Web API")
async def fn_nationalize(arg, p):
	if arg == '':
		return {'text': 'Please supply a name to check'}
	params = {'name': arg}
	async with aiohttp.ClientSession() as session:
		url = 'https://api.nationalize.io/'
		async with session.get(url, params=params) as resp:
			data = await resp.json()
			if data['country'] != []:
				return {'text' : 'Nationalize guesses that "%s" is:\n%s' % (data['name'], '\n'.join(
					[
						chr(127462 + ord(country['country_id'][0]) - 65) + chr(127462 + ord(country['country_id'][1]) - 65) + (" - %f%%" % (country['probability'] * 100))
						for country in data['country']
					]
				))}
			else:
				return {'text' : 'Nationalize doesn\'t what nationality that name is'}

@bot_command(category="Web API")
async def fn_apod(arg, p):
	params = {'api_key': nasa_key}
	async with aiohttp.ClientSession() as session:
		url = 'https://api.nasa.gov/planetary/apod'
		async with session.get(url, params=params) as resp:
			data = await resp.json()
			return {'text' : '%s\n**%s**\n%s' % (data['url'], data['title'], data['explanation'])}

@bot_command(category="Web API")
async def fn_bored(arg, p):
	def to_message(data):
		return {'text': 'You could **%s**!\nAccessibility: %s, Type: %s, Participants: %d, Price: %s, Key %s' % (data['activity'], data['accessibility'], data['type'], data['participants'], data['price'], data['key'])}
	arg = arg.lower()
	params = {'type': arg}
	if arg != '' and arg not in ["education", "recreational", "social", "diy", "charity", "cooking", "relaxation", "music", "busywork"]:
		return {'text': 'Valid types are `education`, `recreational`, `social`, `diy`, `charity`, `cooking`, `relaxation`, `music`, `busywork`'}
	async with aiohttp.ClientSession() as session:
		url = 'http://www.boredapi.com/api/activity'
		if arg == '':
			async with session.get(url) as resp:
				return to_message(await resp.json())
		else:
			async with session.get(url, params=params) as resp:
				return to_message(await resp.json())

@bot_command(category="Web API")
async def fn_foxpic(arg, p):
	async with aiohttp.ClientSession() as session:
		url = 'https://randomfox.ca/floof/'
		async with session.get(url) as resp:
			data = await resp.json()
			return {'text' : '%s' % (data['image'])}

@bot_command(category="Web API")
async def fn_catpic(arg, p):
	async with aiohttp.ClientSession() as session:
		url = 'https://aws.random.cat/meow'
		async with session.get(url) as resp:
			data = await resp.json()
			return {'text' : '%s' % (data['file'])}

@bot_command(category="Web API")
async def fn_meowfact(arg, p):
	async with aiohttp.ClientSession() as session:
		url = 'https://meowfacts.herokuapp.com/'
		async with session.get(url) as resp:
			data = await resp.json()
			return {'text' : '%s' % (data['data'][0])}
command_aliases['catfact'] = 'meowfact'

# -------------------------------------------------------------------

async def run_command(cmd, p):
	""" Attempt to run a command with given arguments """
	cmd = cmd.lower()

	try:
		arg = p['arg']
		if cmd in command_aliases:
			cmd = command_aliases[cmd]
		if cmd in command_handlers:
			if cmd in threaded_commands:
				pass # todo
			else:
				return await command_handlers[cmd](arg, p)

	except Exception as e:
		raise
		return {'text': 'An exception was raised: '+str(e)}
	return None
