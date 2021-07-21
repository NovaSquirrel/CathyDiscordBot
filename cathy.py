from cathy_config import *
from cathy_commands import run_command
import discord, asyncio, json

client = discord.Client()

@client.event
async def on_ready():
	print('We have logged in as {0.user}'.format(client))
	print(client.user.name)
	print(client.user.id)
	print('------')

@client.event
async def on_message(message):
	if message.author == client.user or (message.author.bot and message.author.id != 710925374925570179):
		return

	if message.content.lower().startswith(bot_prefix):
		# extract information from the text
		text = message.content[len(bot_prefix):]

		command = text
		arg = ''
		find_space = text.find(' ')
		find_newline = text.find('\n')
		if find_space >= 0 or find_newline >= 0:
			split_index = min(find_space, find_newline)
			if find_space == -1:
				split_index = find_newline
			if find_newline == -1:
				split_index = find_space
			command = text[0:split_index]
			arg = text[split_index+1:]

		params = {'arg': arg, 'username': message.author.id, 'display_name': message.author.display_name, 'username': message.author.id, 'discord_message': message, 'client': client}
		out = await run_command(command.lower(), params)

		if out == None:
			return
		elif 'markdown' in out:
			await message.channel.send(out['markdown'])
		elif 'text' in out and len(out['text']):
			await message.channel.send(out['text'])
		else:
			await message.channel.send('no text returned')

client.run(config_discord_key)
