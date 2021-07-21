from cathy_config import *
import subprocess, asyncio, discord, random, math, socket, os, io, PIL
from datetime import datetime, timedelta
from PIL import Image, ImageFilter, ImageOps

# Other scripts
from not_constantinople import generate_provinces, generate_settlements
from deeppyer import deepfry
from rotpixels import rotpixels

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

command_handlers = {}	# dictionary of functions to call for each command
command_aliases = {}	# dictionary of commands to change to other commands
hidden_commands = set()

class bot_command(object):
	def __init__(self, f, alias=[]):
		command_name = f.__name__[3:]
		command_handlers[command_name] = f
		for a in alias:
			command_aliases[a] = command_name
	def __call__(self):
		pass

# COMMAND HANDLERS STARTS HERE

@bot_command
async def fn_echo(arg, p):
	return {'text': arg}

@bot_command
async def fn_sq(arg, p):
	return {'text': run_squirrel(arg)}
command_aliases['squirrel'] = 'sq'

@bot_command
async def fn_calc(arg, p):
	return {'text': run_squirrel('print(%s)' % arg)}

@bot_command
async def fn_titlecase(arg, p):
	return {'text': arg.title()}

@bot_command
async def fn_uppercase(arg, p):
	return {'text': arg.upper()}

@bot_command
async def fn_lowercase(arg, p):
	return {'text': arg.lower()}

@bot_command
async def fn_swapcase(arg, p):
	return {'text': arg.swapcase()}

@bot_command
async def fn_random(arg, p):
	param = arg.split(' ')
	if len(param) != 2:
		return {'text': 'Syntax: random min max'}
	else:
		minimum = int(param[0])
		maximum = int(param[1])
		return {'text': str(random.randint(minimum, maximum))}

@bot_command
async def fn_choice(arg, p):
	choices = arg.split('/')
	return {'text': random.choice(choices)}
command_aliases['choices'] = 'choice'
command_aliases['choose'] = 'choice'

@bot_command
async def fn_shuffle(arg, p):
	choices = arg.split('/')
	random.shuffle(choices)
	return {'text': '/'.join(choices)}

@bot_command
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

@bot_command
async def fn_my_ip(arg, p):
	return {'text': 'Running from %s' % subprocess.Popen('hostname -I', shell=True, stdout=subprocess.PIPE).stdout.read().decode()}
hidden_commands.add('my_ip')

@bot_command
async def fn_test(arg, p):
	return {'text': 'Hello!'}

@bot_command
async def fn_chr(arg, p):
	result = ''
	for x in arg.split(' '):
		result += chr(int(x))
	return {'text': result}

@bot_command
async def fn_chrx(arg, p):
	result = ''
	for x in arg.split(' '):
		result += chr(int(x, 16))
	return {'text': result}

@bot_command
async def fn_ord(arg, p):
	result = ''
	for c in arg:
		result += str(ord(c))+" "
	return {'text': result}

@bot_command
async def fn_ordx(arg, p):
	result = ''
	for c in arg:
		result += '%x ' % ord(c)
	return {'text': result}

@bot_command
async def fn_datediff(arg, p):
	two_dates = arg.split(' ')
	if len(two_dates) != 2:
		return {'text': 'Provide two dates to get a difference of, in M/D/Y format, or "now" for the current day'}
	d1 = date_from_string(two_dates[0])
	d2 = date_from_string(two_dates[1])
	difference = abs((d2 - d1).days)
	return {'text': '%d days (%d weeks %d days)' % (difference, difference/7, difference%7)}

@bot_command
async def fn_dateplus(arg, p):
	split = arg.split(' ')
	if len(split) != 2:
		return {'text': 'Provide a date in M/D/Y format and a number of days to add'}
	the_date = date_from_string(split[0]) + timedelta(days=int(split[1]))
	return {'text': the_date.strftime("%m/%d/%Y is a %A")}

@bot_command
async def fn_dayofweek(arg, p):
	the_date = date_from_string(arg)
	return {'text': the_date.strftime("%m/%d/%Y is a %A")}

@bot_command
async def fn_curtime(arg, p):
	return {'text': datetime.today().strftime("Now it's %m/%d/%Y, %I:%M %p")}

@bot_command
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

@bot_command
async def fn_strlen(arg, p):
	return {'text': str(len(arg))}

@bot_command
async def fn_strlenb(arg, p):
	return {'text': str(len(arg.encode('utf-8')))}

@bot_command
async def fn_unicode_name(arg, p):
	if not len(arg):
		return None
	def replace_name(emoji):
		if emoji == '⚧':
			return '**trans rights**'
		else:
			return unicode_name(emoji, 'Not found')
	return {'text': ', '.join(replace_name(x).capitalize() for x in arg[:10])}
command_aliases['emojiname'] = 'unicode_name'
command_aliases['uniname'] = 'unicode_name'

@bot_command
async def fn_random_emoji(arg, p):
	return {'text': '%s %s %s' % random_emoji(8)}
command_aliases['emoji'] = 'random_emoji'

@bot_command
async def fn_random_emojis(arg, p):
	count = 10
	if len(arg) and arg.isnumeric():
		count = int(arg)
	if count > 60:
		count = 60
	return {'text': ''.join(random_emoji(8)[0] for x in range(count))}
command_aliases['emojis'] = 'random_emojis'

@bot_command
async def fn_random_emoji_reacts(arg, p):
	for i in range(10):
		try:
			await p['discord_message'].add_reaction(random_emoji(8)[0])
		except:
			pass
command_aliases['emojireacts'] = 'random_emoji_reacts'

@bot_command
async def fn_eggplant(arg, p):
	await p['discord_message'].add_reaction('🍆')
	return None

@bot_command
async def fn_vote(arg, p):
	await p['discord_message'].add_reaction('👍')
	await p['discord_message'].add_reaction('👎')
	return None

@bot_command
async def fn_reply(arg, p):
	await p['discord_message'].reply('Test')
	return None

@bot_command
async def fn_fakeregionnames(arg, p):
	return {'text': generate_provinces(arg)}

@bot_command
async def fn_fakecitynames(arg, p):
	return {'text': generate_settlements(arg)}

@bot_command
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

@bot_command
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

@bot_command
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

@bot_command
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

@bot_command
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

@bot_command
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

@bot_command
async def fn_joinvoice(arg, p):
	await join_voice_with_user(p['discord_message'].author)
	return None

@bot_command
async def fn_leavevoice(arg, p):
	await leave_voice(p['discord_message'].author)
	return None

@bot_command
async def fn_pause(arg, p):
	guild = p['discord_message'].guild.id
	if guild in voice_clients:
		voice_clients[guild].pause()
	return None

@bot_command
async def fn_stop(arg, p):
	guild = p['discord_message'].guild.id
	if guild in voice_clients:
		voice_clients[guild].stop()
	return None

@bot_command
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

@bot_command
async def fn_barrelroll(arg, p):
	return await play_ffmpeg_audio(p['discord_message'].author, "mp3/doabarrelroll.mp3")

@bot_command
async def fn_cory(arg, p):
	return await play_ffmpeg_audio(p['discord_message'].author, "mp3/cory.mp3")

@bot_command
async def fn_play(arg, p):
	if arg.isalnum():
		return await play_ffmpeg_audio(p['discord_message'].author, "mp3/%s.mp3" % arg)

@bot_command
async def fn_allcommands(arg, p):
	return {'text': ', '.join(x for x in command_handlers if x not in hidden_commands)}

@bot_command
async def fn_help(arg, p):
	return {'text': 'Take a look at https://t.novasquirrel.com/cathy.html'}

@bot_command
async def fn_foresee(arg, p):
	return {'text': 'https://i.ytimg.com/vi/-8gVcI0VAbc/maxresdefault.jpg'}

@bot_command
async def fn_guildemojis(arg, p):
	guild = p['discord_message'].guild
	return {'text': ' '.join([str(x) for x in guild.emojis])}

@bot_command
async def fn_guildemojinames(arg, p):
	guild = p['discord_message'].guild
	return {'text': ' '.join([x.name for x in guild.emojis])}

@bot_command
async def fn_guildemoji(arg, p):
	guild = p['discord_message'].guild
	for emoji in guild.emojis:
		if emoji.name == arg:
			return {'text': str(emoji)}
	else:
		return None

@bot_command
async def fn_clientemoji(arg, p):
	client = p['client']
	for emoji in client.emojis:
		if emoji.name == arg:
			return {'text': str(emoji)}
	else:
		return None

async def image_filter_on_message(message, filter):
	filenames = ["mario", "wario", "luigi", "waluigi", "hamtaro", "sans", "mariokart", "doritos", "fritos", "toast", "burgerking", "aldi", "lidl"]

	if len(message.attachments) == 0:
		return {'text': 'Upload an image with `ca.hamtaro_eat` as the text'}
	else:
		bytes_in_attachment = await message.attachments[0].read()
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
				if filesize >= 8388608:
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
		if len(message.attachments):
			return await image_filter_on_message(message, filter)
		if message.reference and message.reference.resolved:
			return await image_filter_on_message(message.reference.resolved, filter)
		return {'text': 'Upload an image (or reply to an image) with `%s` as the text' % commandname}

@bot_command
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

@bot_command
async def fn_colorize(arg, p):
	colors = parse_color_list(arg, minimum_count = 2)
	async def function(image):
		if len(colors) == 2:
			return ImageOps.colorize(ImageOps.grayscale(image).split()[0], colors[0], colors[1])
		if len(colors) >= 3:
			return ImageOps.colorize(ImageOps.grayscale(image).split()[0], colors[0], colors[2], mid=colors[1])
	return await image_filter_on_msg_or_reply(p['discord_message'], function, 'ca.colorize')

@bot_command
async def fn_solarize(arg, p):
	if(arg == ''):
		arg = 128
	async def function(image):
		return ImageOps.solarize(image.convert('RGB'), int(arg))
	return await image_filter_on_msg_or_reply(p['discord_message'], function, 'ca.solarize')

@bot_command
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

@bot_command
async def fn_grayscale(arg, p):
	async def function(image):
		return ImageOps.grayscale(image)
	return await image_filter_on_msg_or_reply(p['discord_message'], function, 'ca.grayscale')

@bot_command
async def fn_vflip(arg, p):
	async def function(image):
		return ImageOps.flip(image)
	return await image_filter_on_msg_or_reply(p['discord_message'], function, 'ca.vflip')

@bot_command
async def fn_hflip(arg, p):
	async def function(image):
		return ImageOps.mirror(image)
	return await image_filter_on_msg_or_reply(p['discord_message'], function, 'ca.hflip')

@bot_command
async def fn_equalize(arg, p):
	async def function(image):
		return ImageOps.equalize(image)
	return await image_filter_on_msg_or_reply(p['discord_message'], function, 'ca.equalize')

@bot_command
async def fn_invert(arg, p):
	async def function(image):
		return ImageOps.invert(image)
	return await image_filter_on_msg_or_reply(p['discord_message'], function, 'ca.invert')

@bot_command
async def fn_autocrop(arg, p):
	async def function(image):
		return image.crop(image.getbbox())
	return await image_filter_on_msg_or_reply(p['discord_message'], function, 'ca.autocrop')

@bot_command
async def fn_deepfry(arg, p):
	colors = parse_deepfry_colors(arg)
	async def function(image):
		return await deepfry(image, colours = colors, flares = False)
	return await image_filter_on_msg_or_reply(p['discord_message'], function, 'ca.deepfry')

@bot_command
async def fn_deepfry_keepcolor(arg, p):
	colors = parse_deepfry_colors(arg)
	async def function(image):
		return await deepfry(image, colours = None, flares = False)
	return await image_filter_on_msg_or_reply(p['discord_message'], function, 'ca.deepfry_keepcolor')

@bot_command
async def fn_deepfry_flare(arg, p):
	colors = parse_deepfry_colors(arg)
	async def function(image):
		return await deepfry(image, colours = colors, flares = True)
	return await image_filter_on_msg_or_reply(p['discord_message'], function, 'ca.deepfry_flare')

@bot_command
async def fn_thumbnail(arg, p):
	split = arg.split(' ')
	if len(split) < 2:
		return {'text': 'You need to provide a width and a height'}
	width = min(1024, int(split[0]))
	height = min(1024, int(split[1]))

	async def function(image):
		image.thumbnail((width, height))
		return image
	return await image_filter_on_msg_or_reply(p['discord_message'], function, 'ca.thumbnail width height')

@bot_command
async def fn_resize(arg, p):
	split = arg.lower().split(' ')
	if len(split) < 2:
		return {'text': 'You need to provide a width and a height'}
	width = min(1024, int(split[0]))
	height = min(1024, int(split[1]))
	resample = Image.BICUBIC
	if len(split) >= 3:
		if split[2] == 'nearest':
			resample = Image.NEAREST
		elif split[2] == 'box':
			resample = Image.BOX
		elif split[2] == 'linear':
			resample = Image.BILINEAR
		elif split[2] == 'hamming':
			resample = Image.HAMMING
		elif split[2] == 'bicubic':
			resample = Image.BICUBIC
		elif split[2] == 'lanczos':
			resample = Image.LANCZOS

	async def function(image):
		return image.resize((width, height), resample=Image.NEAREST if image.mode == 'P' else resample)
	return await image_filter_on_msg_or_reply(p['discord_message'], function, 'ca.resize width height')

@bot_command
async def fn_rotate(arg, p):
	split = arg.lower().split(' ')
	if arg == '':
		return {'text': 'You need to provide a width and a height'}
	angle = float(split[0])
	resample = Image.BICUBIC
	if len(split) >= 2:
		if split[1] == 'nearest':
			resample = Image.NEAREST
		elif split[1] == 'box':
			resample = Image.BOX
		elif split[1] == 'linear':
			resample = Image.BILINEAR
		elif split[1] == 'hamming':
			resample = Image.HAMMING
		elif split[1] == 'bicubic':
			resample = Image.BICUBIC
		elif split[1] == 'lanczos':
			resample = Image.LANCZOS

	async def function(image):
		return image.rotate(angle, expand=True, resample=Image.NEAREST if image.mode == 'P' else resample)
	return await image_filter_on_msg_or_reply(p['discord_message'], function, 'ca.rotate angle')

@bot_command
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

@bot_command
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

@bot_command
async def fn_sheriff(arg, p):
	message = ".\n"+"⠀ ⠀ ⠀ :cowboy:\n"+"　 %s%s%s\n"+"%s     %s　%s\n"+":point_down: %s%s  :point_down:\n"+"　 %s　%s\n"+"　 %s　 %s\n"+"　 :boot:       :boot:\nHowdy I'm the sheriff of %s"
	if len(arg) == 0:
		arg = random_emoji(8)[0]
	return {"text": message % (arg, arg, arg,arg, arg, arg, arg, arg, arg, arg, arg, arg, arg)}
command_aliases['sherriff'] = 'sherrif'
command_aliases['sherrif'] = 'sherrif'

@bot_command
async def fn_blur(arg, p):
	async def function(image):
		return image.filter(ImageFilter.BLUR)
	return await image_filter_on_msg_or_reply(p['discord_message'], function, 'ca.blur')

@bot_command
async def fn_contour(arg, p):
	async def function(image):
		return image.filter(ImageFilter.CONTOUR)
	return await image_filter_on_msg_or_reply(p['discord_message'], function, 'ca.contour')

@bot_command
async def fn_detail(arg, p):
	async def function(image):
		return image.filter(ImageFilter.DETAIL)
	return await image_filter_on_msg_or_reply(p['discord_message'], function, 'ca.detail')

@bot_command
async def fn_edge_enhance(arg, p):
	async def function(image):
		return image.filter(ImageFilter.EDGE_ENHANCE)
	return await image_filter_on_msg_or_reply(p['discord_message'], function, 'ca.edge_enhance')

@bot_command
async def fn_emboss(arg, p):
	async def function(image):
		return image.filter(ImageFilter.EMBOSS)
	return await image_filter_on_msg_or_reply(p['discord_message'], function, 'ca.emboss')

@bot_command
async def fn_find_edges(arg, p):
	async def function(image):
		return image.filter(ImageFilter.FIND_EDGES)
	return await image_filter_on_msg_or_reply(p['discord_message'], function, 'ca.find_edges')

@bot_command
async def fn_sharpen(arg, p):
	async def function(image):
		return image.filter(ImageFilter.SHARPEN)
	return await image_filter_on_msg_or_reply(p['discord_message'], function, 'ca.sharpen')

@bot_command
async def fn_smooth(arg, p):
	async def function(image):
		return image.filter(ImageFilter.SMOOTH)
	return await image_filter_on_msg_or_reply(p['discord_message'], function, 'ca.smooth')

@bot_command
async def fn_smooth_more(arg, p):
	async def function(image):
		return image.filter(ImageFilter.SMOOTH_MORE)
	return await image_filter_on_msg_or_reply(p['discord_message'], function, 'ca.smooth_more')

@bot_command
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

# -------------------------------------------------------------------

async def run_command(cmd, p):
	""" Attempt to run a command with given arguments """
	cmd = cmd.lower()

	try:
		arg = p['arg']
		if cmd in command_aliases:
			cmd = command_aliases[cmd]
		if cmd in command_handlers:
			return await command_handlers[cmd](arg, p)

	except Exception as e:
		raise
		return {'text': 'An exception was raised: '+str(e)}
	return None
