import discord
import asyncio
import time
import pickle
import os
import json

from cleverbot import Cleverbot
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

import random
import yaml



with open('convos.pk1', 'rb') as c:
	convos = pickle.load(c)


client = discord.Client()


DATE_FORMAT = "%Y-%m-%d"
TIME_FORMAT = "%H:%M:%S"
FULL_DATE = "%Y-%m-%d-%H-%M-%S"


defaultprefix = "."


#voice client- Bad
player = None

log_name = time.strftime(FULL_DATE, time.localtime())





helptext = '''
Here are your commands!

__**Level 0: Normal users**__
Repeat after me: {0}say `thing`
Chatbot: {0}c `message`
Country info: {0}country <args>`[info, land, QOL, econ, loc, army]`
Roll a die: {0}roll `<optional number of sides>`
Radio: {0}play `URL`
BlocSimulator: {0}bloc

__**Level 0: Server Mods**__
ChangeCommandPrefixes: {0}setprefix `newprefix`
Clear chat: {0}clear `<optional number, default is 1000>`

__**Level 0: Server Admins**__
`Insert ideas`
'''

commands = ("say", "c", "country", "roll", "play", "setprefix", "clear", "py", "stop", "todo", "bloc")


async def save_convo(obj):
	with open('convos.pk1', 'wb') as output:
		pickle.dump(obj, output, -1)

async def convo_manager(check):
	if check in convos:
		return convos[check]
	else:
		convos[check] = Cleverbot()
		return convos[check]


async def take_log(message):
	logdir = os.getcwd() + "\\logs\\"
	if message.channel.is_private:
		with open(logdir +log_name +".log", "a", encoding='utf-8') as text_file:
			print("[{0}] Private Message: {1} : ' {2} ' ".format(time.strftime(TIME_FORMAT, time.localtime()), message.author.name, message.content), file=text_file)
		
		print("[{0}] Private Message: {1} : ' {2} ' ".format(time.strftime(TIME_FORMAT, time.localtime()), message.author.name, message.content))
	
	else:
		with open(logdir +log_name +".log", "a", encoding='utf-8') as text_file:
			print("[{0}] {1} in  {2}:{3}: '{4}".format(time.strftime(TIME_FORMAT, time.localtime()), message.author.name, message.channel.server.name,message.channel.name, message.content), file=text_file)
		print("[{0}] {1} in  {2}:{3}: '{4}'".format(time.strftime(TIME_FORMAT, time.localtime()), message.author.name, message.channel.server.name,message.channel.name, message.content))


async def get_nation(url, arg):
	'''if url == "args":
		return `info, land, qol, econ, rep, army`
	'''
	
	NATION_ARGS = {"info":0, "land":1, "qol":2, "econ":3, "rep":4, "army":5}
	
	if arg == "" or arg not in NATION_ARGS:
		return "**Specify with one of the following arguements <info, land, qol, econ, rep, army>**"
	
	req = Request(url, headers={'User-Agent': 'DiscordBot-Human'})
	open_country = urlopen(req).read()
	soup = BeautifulSoup(open_country, "html.parser")
	table = soup.find_all("table", attrs={"class":"table table-striped table-condensed table-hover table-bordered"})
	#soup = BeautifulSoup(str(table), "html.parser")
	
	war_check = ""
	war_country = ""
	super_clean_table = ""
	if arg != "":
		for t in table[NATION_ARGS[arg]]:
			clean_table = BeautifulSoup(str(t), "html.parser")
			war_check += clean_table.prettify()
			super_clean_table += clean_table.get_text()
			#super_clean_table = clean_table.strings().replace("\n", "")
		#return super_clean_table.replace("\n\n", "\n")
	else:
		return "Something went wrong :("
	
	if arg == "army" and "at peace" not in super_clean_table.lower():
		new_soup = BeautifulSoup(war_check, "html.parser")
		for link in new_soup.findAll('a'):
			if "#" not in link.get('href'):
				war_country += link.get('href')
				
		return super_clean_table.replace("\n\n", "\n") + "\n" + "http://www.blocgame.com"+ war_country
	
	return super_clean_table.replace("\n\n", "\n")


async def parse_urban(word):
	pass


#Prefix bs
async def create_prefix(server):
	cfg_name = 'config.yml'
	default_cfg = { server.id: {"prefix":defaultprefix}}
	
	with open(cfg_name, 'r') as f:
		config = yaml.load(f)#
	
	
	try:
		if server.id in list(config):
			already_prefix = True
		
		if not already_prefix:
			with open(cfg_name, "a") as cfg:
				yaml.dump(default_cfg, cfg, default_flow_style=False)
				return
		
	except TypeError as e:
		print(e)

async def get_prefix(server):
	try:
		ID = server.id
		
		with open('config.yml', 'r') as config:
			loadedcfg = yaml.load(config)
			
		return loadedcfg[ID]['prefix']
	except KeyError:
		await create_prefix(server)
	except AttributeError:
		print("stop being a little bitch")

async def update_prefix(server, prefix):
	with open("config.yml") as f:
		list_doc = yaml.load(f)

	if list_doc[server.id]:
		list_doc[server.id]['prefix'] = prefix

	with open("config.yml", "w") as f:
		yaml.dump(list_doc, f, default_flow_style=False)





@client.event
async def on_message(message):
	if not message.channel.is_private:
		prefix = await get_prefix(message.server)
	else:
		prefix = defaultprefix
		
	global player
		
		
	if message.content.startswith(prefix) and not message.content.startswith(prefix+prefix):
		for i in commands:
			if message.content.startswith(prefix + i):
				await take_log(message)
		
	#strr.count('\n')
	if message.author == client.user:
		if message.content.count('\n') >= 10 and not message.channel.is_private:
			temp_msg = message
			warn_msg = await client.send_message(message.channel, "^ That message will be deleted in 100s for being too long. This is an experimental feature as not to clog chat")
			await asyncio.sleep(100)
			await client.delete_message(temp_msg)
			await client.delete_message(warn_msg)
		
		return
	
	if message.author.bot:
		return
		
		
	#Triggers
	if message.content == client.user.mention:
		print(message.author.name + " mentioned you!")
		await client.send_message(message.author, helptext.format(prefix))
		
	if client.user.mention in message.content:
		await take_log(message)
		
	if 'oshit' in message.content.lower():
		if 'OSHIT' in message.content:
			await client.send_message(message.channel, "WADDUP")
			return
				
		await client.send_message(message.channel, "waddup")
		
	if 'cyka' in message.content.lower() and 'blyat' not in message.content.lower():
		await client.send_message(message.channel, 'Блять')
		
	if 'ayy' in message.content.lower() and 'lmao' not in message.content.lower():
		await client.send_message(message.channel, "lmao")
		
	if 'lmao' in message.content.lower():
		await client.send_message(message.channel, "ayy")
	
	if 'kill all bots' in message.content.lower():
		await client.send_message(message.channel, "Tracing {}'s IP...".format(message.author.mention))
		await asyncio.sleep(5)
		await client.send_message(message.channel, "Ddox beginning.." )
	
	if '/o/' in message.content.lower():
		await client.send_message(message.channel, "\\o\\")
		
	if '\\o\\' in message.content.lower():
		await client.send_message(message.channel, "/o/")
	
	if '/o\\' in message.content.lower():
		await client.send_message(message.channel, '\\o/')
	
	if '\\o/' in message.content.lower():
		await client.send_message(message.channel, '/o\\')
		
	if message.content.lower().startswith("good boy"):
		await client.send_message(message.channel, "Thanks!")
		
	if message.content.lower().startswith("wew") and "lad" not in message.content.lower():
		if "WEW" in message.content:
			await client.send_message(message.channel, "LAD")
			return
		await client.send_message(message.channel, "lad")
		
		
	#Commands
	
	#Fun
	if message.content.lower().startswith(prefix + "help"):
		try:
			await client.send_message(message.author, helptext.format(prefix))
		except TypeError:
			print("Still being a little bitch")
	
	if message.content.lower().startswith(prefix + "say "):
		await client.send_message(message.channel, " ".join(message.content.split()[1:]))
	
	if message.content.lower().startswith(prefix + "roll"):
		if len(message.content.split()) >= 2:
			if message.content.split()[1].isdigit():
				num = message.content.split()[1]
				await client.send_message(message.channel, "{}".format(random.randint(1, num)))
				return
			else:
				await client.send_message(message.channel, ":x:Invalid argument")
				return
		else:
			await client.send_message(message.channel, "{}".format(random.randint(1, 6)))
			return
		
	if message.content.lower().startswith(prefix + "c "):
		await client.send_typing(message.channel)
		c = await convo_manager(message.author)
		try:
			await client.send_message(message.channel, c.ask(" ".join(message.content.split()[1:])))
			await save_convo(convos)
		except UnicodeEncodeError as e:
			await client.send_message(message.channel, "I don't really like emoji atm")
		
		
	#Useful
	if message.content.lower().startswith(prefix + "urban "):
		if  not len(message.content.split()) >= 2:
			await client.send_message(message.channel, "Word?")
			return
		#parse_urban
		#parse json from http://api.urbandictionary.com/v0/define?term= + " ".join(message.content.split()[1:])
	
	if message.content.lower().startswith(prefix + "country "):
		
		if len(message.content.split()) >= 2:
			m = message.content.split()[1]
			if len(message.content.split()) >= 3:
				arg = message.content.split()[2]
			else:
				await client.send_message(message.channel, "Specify with an arguement `<info, land, qol, econ, rep, army>`" )
				return
		else:
			await client.send_message(message.channel, "I need a country url here")
			return
		
		try:
			if m.isdigit() :
				fullm = "http://blocgame.com/stats.php?id=" + m
				info = await get_nation(fullm, arg)
				await client.send_message(message.channel, "Getting info from http://blocgame.com/stats.php?id=" + m + "\n" +info)
			elif "blocgame.com/stats.php?id=" in m:
				await client.send_message(message.channel, )
				info = await get_nation(m, arg)
				await client.send_message(message.channel, "Getting info from "+ m + "\n" + info)
			else:
				await client.send_message(message.channel, "Bad nation link/number")
		except IndexError:
			await client.send_message(message.channel, "That nation does not exist")
		
	if message.content.lower().startswith(prefix + "play "):
		
		await client.send_message(message.server, ":x:Disabled due to bandwith issues")
		if "youtube.com/watch?v=" not in message.content:
			await client.send_message(message.server, "But that should be a youtube url")
			if message.author.voice_channel == None:
				await client.send_message(message.channel, "Also you must be in a voice channel")
				return
			else: 
				return
		if message.author.voice_channel == None:
				await client.send_message(message.channel, "Also you must be in a voice channel")
						
		#Wew rewrite all this
		'''
		if player == None:
			print()
		elif player.is_playing():
			await client.send_message(message.channel, "Something is already playing")
			return
		
		if message.author.voice_channel == None:
			await client.send_message(message.channel, "`You must be in a voice channel!`")
			return
			
		if "youtube.com/watch?v=" not in message.content.split()[1]:
			await client.send_message(message.channel, "Currently only accepting YouTube:tm: urls")
			return
		
		voice = await client.join_voice_channel(message.author.voice.voice_channel)
		#Play music
		player = await voice.create_ytdl_player(message.content.split()[1])
		await client.send_message(message.channel, "Now playing: `" +  player.title + "`" )
		player.start()
		#await voice.disconnect()
		#await client.send_message(message.channel, "Finished playing: `" +  player.title + "`" )
		#player = None
		
	if message.content.lower().startswith(prefix + "skip"):
		await take_log(message)
		if player == None:
			await client.send_message(message.channel, "Nothing is currently playing!")
			return
		else:
			await player.stop()
			#await voice.disconnect()
			#player == None
		'''
	
	'''
	if message.content.lower().startswith(prefix + "checkperms"):
		await take_log(message)
		if(message.channel.permissions_for(message.author)).managage_server:
			print("11113241")
	'''
		
		
		
	#Mods
	if message.content.lower().startswith(prefix + "setprefix "):
		if not message.channel.permissions_for(message.author).manage_server:
			await client.send_message(message.channel, "You do not have permission to do this!")
			return
		
		await update_prefix(message.server, " ".join(message.content.split()[1:]))
		await client.send_message(message.channel, "New prefix set: " + await get_prefix(message.server))
		
	if message.content.lower().startswith(prefix + "clear" ):
		if not message.channel.permissions_for(message.author).manage_server:
			await client.send_message(message.channel, "No permission!")
			return
		
		deleted = 0
		num = 1000
		if len(message.content.split()) >= 2:
			if message.content.split()[1].isdigit():
				num = message.content.split()[1]
			else:
				await client.send_message(message.channel, "Invalid argument")
				return
					
		
		try:
			async for log in client.logs_from(message.channel, limit=num):
				await client.delete_message(log)
				deleted += 1
			
		except discord.errors.Forbidden:
			await client.send_message(message.channel, "I need to Manage Messages permission to remove all messages. Removing my messages only")
			async for log in client.logs_from(message.channel, limit=num):
				if log.author == client.user:
					client.delete_message(log)
					deleted += 1
		except Exception as e:
			await client.send_message(message.channel, ":x: Something went wrong :(")
			print(e)
			
		if deleted:
			await client.send_message(message.server, "Deleted {} messages".format(deleted))
		
		
	#Owner
	if message.content.lower().startswith(prefix + "todo "):
		if str(message.author.discriminator) == "9162":
			if message.content.split()[1] == "readall":
				outfile = open("todo.txt", "r")
				await client.send_message(message.channel, outfile.readlines())
				return
			else:
				with open("todo.txt", "a") as todofile:
					print(" ".join(message.content.split()[1:]), file=todofile)
					return
		else:
			await client.send_message(message.channel, "Only the Bot Owner can do that!" )
			return
		
	if message.content.lower().startswith(prefix + "py "):
		if str(message.author.discriminator) == "9162":
			cmd = message.content.replace(prefix+"py","")
			eval(cmd)
		else:
			await print("It was not very succesful")
			await client.send_message(message.channel, "Only the Bot Owner can do that!" )
		
	if message.content.lower().startswith(prefix + "stop" ):
		if str(message.author.discriminator) == "9162":
			await client.send_message(message.channel, "Bye!")
			await client.logout()
		else:
			await print("It was not very succesful")
			await client.send_message(message.channel, "Only the Bot Owner can do that!" )




@client.event
async def on_server_join(server):
	await create_prefix(server)

@client.event
async def on_ready():
	print(time.strftime(DATE_FORMAT, time.localtime()))
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	print("https://discordapp.com/oauth2/authorize?&client_id="+client.user.id +"&scope=bot&permissions=3688992")
	print('------')

try:
	client.run('token')
except ConnectionResetError:
	print("Connection issues")

