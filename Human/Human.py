# -*- coding: utf-8 -*-
import asyncio
import discord
from cleverbot import Cleverbot
from bs4 import BeautifulSoup
import markovify
import yaml
from gingerit.gingerit import GingerIt
#  import feedparser


import time  # *Switch all time to datetime
import datetime
import aiohttp
import pickle
import random
import os
import inspect
import re

start = datetime.datetime.now()


class StartupErr(Exception):
    pass


class Args(list):
    async def toString(self):
        return " ".join(self)


class Bot:
    def __init__(self):
        self.bootup = self.boot()
        self.name = "Human"
        self.author = '@Yu#9162'
        self.library = 'discord.py'
        self.source = 'https://github.com/Kyu/Human'
        self.invite = "https://discordapp.com/oauth2/authorize?&client_id=210448501748924416&scope=bot&permissions=-1"
        self.version = 'Beta0.8'
        self.config_name = 'config.yml'
        self.start = datetime.datetime.now()
        self.commandsrun = 0
        self.lastsaid = {}
        self.defaultprefix = "."# *Find something better
        self.setting_format = {"prefix": ".", "clear": 100, "silent": [],
                               "disabled": [], "default_roles": [],
                               "disabled_commands": [], "mod_log": ""}
        self.TIME_FORMAT = "%H:%M:%S"
        self.DATE_FORMAT = '%Y-%m-%d'
        self.log_name = self.start.strftime('%Y-%m-%d-%H-%M-%S') + ".log"
        self.log_dir = os.getcwd() + "/logs/" + self.log_name
        self.commands = ('purge', 'blacklist', 'reload', 'say', 'roll', 'c',
                         'flip', 'play', 'clear', 'py', 'stop',
                         'todo', 'bloc', 'suggestion', '8ball', 'stats',
                         'whosaid', 'case', 'reverse', 'settings', 'setting',
                         'country', 'eval', 'grammar', 'meow', 'doggo', 'dog',
                         'puppy', 'kitty', 'kitten', 'ping', 'g', 'mentions',
                         'mention', 'mentioned', 'info', "invite", "kick",
                         "ban")
        self.suggest_timeout = {}
        self.allow_convos = {}
        self.loadConvos()
        self.loadSettings()
        self.rss = {}  # *Unused

    def boot(self):
        files = ['config.yml', 'todo.txt', 'convos.pk1']
        for file in files:
            if not os.path.exists(file):
                open(file, 'w').close()

        if os.path.exists('logs'):
            pass
        else:
            try:
                os.makedirs('logs')
            except OSError:
                raise StartupErr("logs folder")

        return True

    def loadSettings(self):
        with open('config.yml', 'r') as config:
            sess = yaml.load(config)
        if type(sess) is dict:
            self.settings = sess
        elif sess is None:
            sess = dict()
            sess['blacklist'] = []
            with open(self.config_name, "w") as cfg:
                yaml.dump(sess, cfg, default_flow_style=False)
            self.settings = sess
        else:
            raise StartupErr("Something is wrong with your config")
        self.blacklist = self.settings['blacklist']

        return True

    def update_server(self, server):
        settings = {"prefix": self.defaultprefix, "clear": 100, "silent": [],
                    "disabled": [], "default_roles": [],
                    "disabled_commands": [], "mod_log": ""}

        updated = []

        for i in self.setting_format:
            if i not in self.settings[server.id]:
                self.settings[server.id][i] = settings[i]
                updated.append(i)

        self.reload_settings()

        if updated:
            return "Updated: {0} in {1.name}".format(", ".join(updated), server)
        else:
            return "Nothing to update in {0.name}".format(server)

    def reload_settings(self):
        with open(self.config_name, "w") as cfg:
            yaml.dump(self.settings, cfg, default_flow_style=False)

    def info(self):
        return '''Author: {0.author}
Library: {0.library}
Version: {0.version}
Source: {0.source}
Invite: {0.invite}
Server: https://discord.gg/2MqkeeJ
        '''.format(self)

    def loadConvos(self):
        try:
            with open('convos.pk1', 'rb') as runs:
                cv = pickle.load(runs)
        except EOFError:
            self.convos = {}
            return True
        if type(cv) is dict:
            self.convos = cv
        elif type(cv) is None:
            cv = dict()
            self.convos = cv
        else:
            raise StartupErr("Something is wrong with convos")
        return True

    def owner(self, user):
        if type(user) == discord.User:
            if user.id == '142510125255491584':
                return True

    def helpText(self):
        return '''
Here are your commands!
The prefix for this Server: {1.name} is `{0}`

__**Level 0: Normal users**__
Repeat after me: {0}say `thing`
See who last used {0}say: `{0}whosaid`
Chatbot: {0}c `message`
Country info: {0}country <args>`[info, land, QOL, econ, loc, army]`
Roll a die: {0}roll `<optional number of sides>`
Flip a coin: {0}flip
Radio: {0}play `URL`
Magic 8-ball:{0}8ball `query`
BlocSimulator: {0}bloc
Stats: {0}stats
Bot info: {0}info
New Quote: {0}case `thing`
Reverse a sentence: {0}reverse `sentence`
View a quote: {0}case `thing` |also comes with [tell me about] `thing`|
See past mentions: {0}mentions `optional number`
Grammar checker: {0}grammar `thing` | Aliases : {0}g
Invite link: {0}invite



__**Level 0: Server Mods**__
Clear chat: {0}clear `<optional number, default is 100>` `optional User/id`
View Settings: {0}settings `optional arg[clear, silent, disabled, prefix]`
Change a setting: {0}setting `setting name` `value` | Do {0}setting `info` to view what you settings can change
Send a suggestion: {0}suggestion `suggestion`
Kick a user: {0}kick `@User/userid` optional reason
Ban a user: {0}kick `@User/userid` optional reason  | optional purge=n

Bot Discord:
https://discord.gg/2MqkeeJ
'''


bot = Bot()
parser = GingerIt()
client = discord.Client()


async def suggest_reset():
    while True:
        await asyncio.sleep(86400)
        bot.suggest_timeout = {}


async def who_said(channel):
    try:
        return "{} made me do it!".format(bot.lastsaid[channel].mention)
    except KeyError:
        return ":x: The perpetrator has vanished :x:"


async def sent_from(channel, name):
    bot.lastsaid[channel] = name


async def correctGrammar(text):
    correctedgrammar = parser.parse(text)
    return correctedgrammar


async def fortune():
    poss = ["It is certain",
            "It is decidedly so",
            "Without a doubt",
            "Yes, definitely",
            "You may rely on it",
            "As I see it, yes",
            "Most likely",
            "Outlook good",
            "Yes",
            "Signs point to yes",
            "Reply hazy try again",
            "Ask again later",
            "Better not tell you now",
            "Cannot predict now",
            "Concentrate and ask again",
            "Don't count on it",
            "My reply is no",
            "My sources say no",
            "Outlook not so good",
            "Very doubtful"]

    return poss[random.randint(0, 19)]


async def getDoggo():
    doggo = 'random.dog/ doggo'
    return doggo


async def getKitty():
    kitty = 'random.cat/ kitty'
    return kitty


async def save_convo(obj):
    with open('convos.pk1', 'wb') as output:
        pickle.dump(dict(obj), output, -1)
    return


async def convo_manager(check):
    if check in bot.convos:
        return bot.convos[check]
    else:
        # *Creates a conversation for them if not
        bot.convos[check] = Cleverbot()
        return bot.convos[check]

async def bot_chat(channel, chatters=2):
    prompt = "Hi"
    prefixes = [":speech_balloon:", ":thought_balloon:", ":cloud_lightning:", ":diamond_shape_with_a_dot_inside:", ":thinking:", ":sunglasses:", ":poop:", ":eye_in_speech_bubble:", ":speech_left:", ":eyes:", ":robot:", ":no_mouth:", ":globe_with_meridians:", ":capital_abcd:", ":interrobang:"]
    
    if chatters > len(prefixes):
        return "Too much bots. Max is {}".format(len(prefixes))
    
    while bot.allow_convos[channel.id]:
        for i in range(1, chatters+1):
            pr = "{0}Chatter: {1}".format(channel.id, i)
            c = await convo_manager(pr)
            prompt = c.ask(prompt)
            await client.send_message(channel, "{0} {1}".format(prefixes[i], prompt))
            await asyncio.sleep(3)
        
        await save_convo(bot.convos)
    
    return "Convo Done"        

# *Log better
async def take_log(message):
    logdir = os.getcwd() + "/logs/"

    try:
        if message.channel.is_private:
            with open(bot.log_dir,
                      "a+", encoding='utf-8') as text_file:
                print("[{0}] Private Message: {1} : ' {2} ' "
                      .format(time.strftime(bot.TIME_FORMAT, time.localtime()),
                              message.author.name, message.content),
                      file=text_file)

            print("[{0}] Private Message: {1} : ' {2} ' "
                  .format(time.strftime(bot.TIME_FORMAT, time.localtime()),
                          message.author.name, message.content))

        else:
            with open(bot.log_dir,
                      "a+", encoding='utf-8') as text_file:
                print("[{0}] {1} in  {2}:{3}: '{4}"
                      .format(time.strftime(bot.TIME_FORMAT,
                              time.localtime()), message.author.name,
                              message.channel.server.name,
                              message.channel.name, message.content),
                      file=text_file)
            print("[{0}] {1} in  {2}:{3}: '{4}'"
                  .format(time.strftime(bot.TIME_FORMAT, time.localtime()),
                          message.author.name, message.channel.server.name,
                          message.channel.name, message.content))
    except UnicodeEncodeError:
        with open(bot.log_dir + bot.log_name,
                  "a+", encoding='utf-8') as text_file:
                print("[{0}] Message UnicodeErr: {1} : ' {2} ' "
                      .format(time.strftime(bot.TIME_FORMAT, time.localtime()),
                              message.author.id, message.content),
                      file=text_file)


async def get_nation(url, arg):
    '''if url == "args":
        return `info, land, qol, econ, rep, army`
    '''
    NATION_ARGS = {"info": 0, "land": 1, "qol": 2, "econ": 3, "rep": 4,
                   "army": 5}

    if arg == "" or arg not in NATION_ARGS:
        return ("**Specify with one of the following arguments:"
                " <info, land, qol, econ, rep, army>**")
    try:
        async with aiohttp.get(url) as req:
            if req.status == 200:
                open_country = await req.text()
        soup = BeautifulSoup(open_country, "html.parser")
        table = soup.find_all("table", attrs={"class": """table table-striped
                                              table-condensed table-hover
                                              table-bordered"""})
    except Exception as e:
        return ":x:{}:x:".format(str(e))

    war_check = ""
    war_country = ""
    super_clean_table = ""
    if arg != "":
        for t in table[NATION_ARGS[arg]]:
            clean_table = BeautifulSoup(str(t), "html.parser")
            war_check += clean_table.prettify()
            super_clean_table += clean_table.get_text()
    else:
        return "Something went wrong :("

    if arg == "army" and "at peace" not in super_clean_table.lower():
        new_soup = BeautifulSoup(war_check, "html.parser")
        for link in new_soup.findAll('a'):
            if "#" not in link.get('href'):
                war_country += link.get('href')

        return (super_clean_table.replace("\n\n", "\n") +
                "\n" + "http://www.blocgame.com" + war_country)

    return super_clean_table.replace("\n\n", "\n")


async def bloc_speaks(prompt=""):
    # Mem leak here
    try:
        with open(os.getcwd() + '/BlocSim/BlocSpeaks.txt',
                  'r', encoding='utf-8') as f:
            text = f.read()
    except FileNotFoundError:
        print("File not found")
        return
    text_model = markovify.NewlineText(text)  # *, state_size=4)
    try:
        if prompt:
            sentence = text_model.make_sentence_with_start(prompt)
            return sentence
        else:
            sentence = text_model.make_sentence()
            return sentence
    except Exception as e:
        return (e)


async def stats():
    uptime = str(datetime.datetime.now() - bot.start).split(".")[0]
    servers = len(client.servers)
    return '''Uptime: {0}
Commands Run: {1}
Servers Joined: {2}
Running Conversations: {3}
'''.format(uptime, bot.commandsrun, servers, len(bot.convos))


async def set(server, case, rule):
    cases = {'prefix': 'The command prefix for this server',
             'clear': 'How much messages the clear command removes by default',
             'silent': 'Channels where the bot only responds to commands',
             'disabled': 'Channels where the bot doesn\'t talk at all',
             'default_roles': "The role(s) new users automatically get",
             "disabled_commands": "Commands disabled on the server",
             "mod_log": "Channel where the bot logs mod actions"}
            # "bot_commanders": "Users able to do bot level commands"}

    if case == 'info':
        if type(rule) is str and rule:
            return cases[rule]
        else:
            return "You can check for {} ".format(", ".join(cases))

    if not rule:
        return "You need to enter what you want the setting to be changed to!"

    if case not in cases:
        return "Invalid setting!"

    with open(bot.config_name, 'r') as f:
        config = yaml.load(f)
    # TODO PREFIX
    if server.id in config:
        if case == 'mod_log' or case == 'prefix':
            if type(rule) is str:
                config[server.id][case] = rule
            else:
                return "Invalid setting"

        if case == 'clear':
            if rule.isdigit():
                config[server.id][case] = int(rule)
            else:
                return "{} is not a number".format(rule)

        if case == 'silent' or case == 'disabled':
            try:
                rule = rule.id
            except:
                pass
            if rule.isdigit():
                if rule in config[server.id][case]:
                    config[server.id][case].remove(rule)
                    action = 'removed from'
                else:
                    config[server.id][case].append(rule)
                    action = 'added to'
            else:
                return "Invalid rule {}".format(rule)
        if (case == 'silent' or case == 'disabled'
                or case == 'default_roles' or case == 'disabled_commands'):
            if type(rule) is str:
                try:
                    if rule in config[server.id][case]:
                        config[server.id][case].remove(rule)
                        action = 'removed from'
                    else:
                        config[server.id][case].append(rule)
                        action = "added to"
                except KeyError:
                    config[server.id][case] = [rule]
                    action = "created for"
            else:
                return "Enter a valid setting"
    else:
        await create_server(server)
        case = 'create'
        return """Server rules have just been created. Do {}settings to view them
        """.format(bot.defaultprefix)
    with open(bot.config_name, "w") as cfg:
        yaml.dump(config, cfg, default_flow_style=False)
        bot.loadSettings()

    if case == 'prefix' or case == 'mod_log':
        return "{0} set to {1}".format(case, bot.settings[server.id][case])

    if case == 'clear':
        return "Clear amount set to {}".format(bot.settings[server.id][case])

    return '{0} {1} {2} list'.format(rule, action, case)


async def create_server(server):
    cfg_name = 'config.yml'
    default_cfg = {server.id: bot.setting_format}

    with open(cfg_name, 'r') as f:
        config = yaml.load(f)

    try:
        if server.id in list(config):
            return

        with open(cfg_name, "a") as cfg:
            yaml.dump(default_cfg, cfg, default_flow_style=False)
            bot.loadSettings()
            return
    except TypeError as e:
        print("Error on creating server: {}"
              .format(type(e).__name__ + ': ' + str(e)))


async def blacklist(obj):
    with open("config.yml") as f:
        list_doc = yaml.load(f)

    if obj not in list_doc['blacklist']:
        list_doc['blacklist'].append(obj)
    else:
        list_doc['blacklist'].remove(obj)

    with open("config.yml", "w") as f:
        yaml.dump(list_doc, f, default_flow_style=False)

    bot.loadSettings()


@client.event
async def on_message(message):
    if not message or not message.content:
        return
    
    if message.author.id in bot.blacklist:
        return

    prefix = bot.defaultprefix

    if not message.channel.is_private:
        if message.server.id in bot.blacklist:
            return
        if message.channel.id in bot.settings[message.server.id]['disabled']:
            return
        if message.server.id not in bot.settings:
            await create_server(message.server)

        prefix = bot.settings[message.server.id]['prefix']

    if message.author == client.user:
        await take_log(message)

        if (message.content.count('\n') >= 10 and
                not message.channel.is_private):
            temp_msg = message
            warn_msg = await client.send_message(message.channel,
                                                 ("^ That message will be "
                                                  "deleted in 30s for "
                                                  "being too long. This an "
                                                  "an experimental feature as "
                                                  "not to clog chat "))
            await asyncio.sleep(5)
            await client.delete_message(warn_msg)
            await asyncio.sleep(25)
            await client.delete_message(temp_msg)
        return

    if message.author.bot:
        return

    for i in bot.commands:
        if message.content.lower().split()[0] == prefix + i:
            if i in bot.settings[message.server.id]["disabled_commands"]:
                return
            args = (Args(message.content.split()[1:])
                    if message.content.split()[1:] else None)
            bot.commandsrun += 1
            await take_log(message)

    # *Triggers
    if message.content == client.user.mention:
        print(message.author.name + " mentioned you!")
        await client.send_message(message.author,
                                  bot.helpText().format(prefix, message.server)
                                  )

    if client.user.mention in message.content:
        await take_log(message)

    if message.content.lower().split()[0] == prefix + '8ball':
        if not args:
            await client.send_message(message.channel,
                                      "Actually there are only 7 dragon balls")
            return
        await client.send_message(message.channel, await fortune())

    if message.content.lower().split()[0] == prefix + 'say':
        if args is None:
            return
        await sent_from(message.channel.id, message.author)
        await client.send_message(message.channel,
                                  message.content.replace(prefix + "say", "", 1
                                                          ))

    if message.content.lower().split()[0] == prefix + 'reverse':
        await client.send_message(message.channel,
                                  '\u202e{}'.format(await args.toString()))

    if message.content.lower().split()[0] == prefix + "whosaid":
        await client.send_message(message.channel,
                                  await who_said(message.channel.id))

    if message.content.lower().split()[0] == prefix + "flip":
        if random.choice([0, 1]):
            await client.send_message(message.channel,
                                      "You flipped for Heads!")
        else:
            await client.send_message(message.channel,
                                      "You flipped for Tails!")

    if (message.content.lower().split()[0] == prefix + 'grammar' or
            message.content.lower().split()[0] == prefix + 'g'):

        msg = await client.send_message(message.channel, "*{}*"
                                        .format(await args.toString()))

        corrected = await correctGrammar(await args.toString())

        await client.edit_message(msg, "*{0}* :arrow_right: **{1}**"
                                       .format(msg.content,
                                               corrected['result']))

    # *Add text randomnisation
    # *remove max, change message
    if message.content.lower().split()[0] == prefix + 'roll':
        roll = 6
        if args:
            try:
                if int(args[0]) >= 1:
                    roll = 120 if int(args[0]) >= 120 else int(args[0])
            except ValueError:
                await client.send_message(message.channel,
                                          ("I said **_number of sides_**\nDo "
                                           "you even know what a number is {}?"
                                           .format(message.author.mention)))
                return
        await client.send_message(message.channel,
                                  "Rolled a {0}".format(random.randint(1, roll)
                                                        ))

    if message.content.lower().split()[0] == prefix + 'c':
        await client.send_typing(message.channel)
        try:
            c = await convo_manager(message.author)
            await client.send_message(message.channel,
                                      c.ask(await args.toString()))
            await save_convo(bot.convos)
        except UnicodeEncodeError as e:
            await client.send_message(message.channel,
                                      "I don't really like emoji atm")
        except ConnectionError:
            await client.send_message(message.channel,
                                      (":x: Oops something went wrong! "
                                       "Is the bot server down?"))

    if message.content.lower().split()[0] == prefix + 'bloc':
        if args:
            if len(args) > 2:
                await client.send_message(message.channel,
                                          ":x:Prompt can only be 1 or 2 words long:x:")
                return
            prompt = await args.toString()
            await client.send_message(message.channel,
                                      await bloc_speaks(prompt=prompt))
            return
        await client.send_message(message.channel, await bloc_speaks())
    # *Useful
    if message.content.lower().split()[0] == prefix + 'help':
        msg = await client.send_message(message.channel,
                                        """Help Sent to {}!"""
                                        .format(message.author.mention))
        await client.send_message(message.author,
                                  bot.helpText()
                                  .format(prefix, message.server))
        await asyncio.sleep(15)
        await client.delete_message(msg)

    if message.content.lower().split()[0] == prefix + "invite":
        await client.send_message(message.channel, bot.invite)

    if message.content.lower().split()[0] == prefix + 'info':
        await client.send_message(message.channel, bot.info())

    if message.content.lower().split()[0] == prefix + 'ping':
        pong = await client.send_message(message.channel, "Ow!")
        ping = pong.timestamp - message.timestamp
        await client.edit_message(pong,
                                  "Response took 0{}s"
                                  .format((str(ping).split(':')[2])
                                          .strip('0')))

    if message.content.lower().split()[0] == prefix + "suggestion":
        if not args:
            await client.send_message(message.channel,
                                      ("Do nothing is a great suggestion. "
                                       "I'll do that all day"))
            return

        try:
            if bot.suggest_timeout[message.author.id] >= 5:
                await client.send_message(message.channel,
                                          "Enough suggestions for today {}."
                                          .format(message.author.mention))
                return
        except KeyError:
            bot.suggest_timeout[message.author.id] = 1

        bot.suggest_timeout[message.author.id] += 1
        with open("todo.txt", "a") as todofile:
            print("[Suggestion from]{0}: {1}"
                  .format(message.author.name, await args.toString()),
                  file=todofile)

    if (message.content.lower().split()[0] == prefix + 'cat' or
            message.content.lower().split()[0] == prefix + 'meow' or
            message.content.lower().split()[0] == prefix + 'kitten' or
            message.content.lower().split()[0] == prefix + 'kitty'):
        await client.send_message(message.channel, await getKitty())

    if (message.content.lower().split()[0] == prefix + 'pupper' or
            message.content.lower().split()[0] == prefix + 'doggo' or
            message.content.lower().split()[0] == prefix + 'dog' or
            message.content.lower().split()[0] == prefix + 'puppy'):
        await client.send_message(message.channel, await getDoggo())

    # *Finish this
    if message.content.lower().split()[0] == prefix + "urban":
        if not len(message.content.split()) >= 2:
            await client.send_message(message.channel, "Word?")
            return
        # *parse json from http://api.urbandictionary.com/v0/define?term= + " ".join(message.content.split()[1:])

    if message.content.lower().split()[0] == prefix + "country":
        if args:
            m = args[0]
            try:
                args[1]
            except IndexError:
                await client.send_message(message.channel,
                                          "Specify with an argument `<info, land, qol, econ, rep, army>`")
                return
        else:
            await client.send_message(message.channel,
                                      "I need a country url here")
            return

        try:
            if m.isdigit():
                fullm = "http://blocgame.com/stats.php?id=" + m
                info = await get_nation(fullm, args[1])
                await client.send_message(message.channel,
                                          "Getting info from http://blocgame.com/stats.php?id=" +
                                          m + "\n" + info)
            elif "blocgame.com/stats.php?id=" in m:
                info = await get_nation(m, args[1])
                await client.send_message(message.channel,
                                          "Getting info from " +
                                          m + "\n" + info)
            else:
                await client.send_message(message.channel,
                                          "Bad nation link/number")
        except IndexError:
            await client.send_message(message.channel,
                                      "That nation does not exist")

    if message.content.lower().split()[0] == prefix + "play":
        await client.send_message(message.channel,
                                  ":x:Disabled due to bandwith issues")

    if message.content.lower().split()[0] == prefix + "stats":
        await client.send_message(message.channel, await stats())

    if (message.content.lower().split()[0] == prefix + 'mentions' or
            message.content.lower().split()[0] == prefix + 'mentioned'):
        try:
            n = int(args[0]) if args else 1000
        except ValueError:
            await client.send_message(message.channel, "Invalid argument!")
            return
        finally:
            n = 2000 if n > 1999 else n

        mentions = []

        async for msg in client.logs_from(message.channel, limit=n):
            if message.author.mentioned_in(msg):  # or other things
                mentions.append(
                    "`{0}:{1}` |`{2}` at `{3}UTC`\n```css\n{4}: {5}```\n"
                    .format(msg.server, msg.channel,
                            ((str(msg.timestamp).split('.'))[0]).split()[0],
                            ((str(msg.timestamp).split('.'))[0]).split()[1],
                            msg.author, msg.clean_content))
        if mentions:
            mentions = Args(mentions)
            await client.send_message(message.author,
                                      await mentions.toString())
        else:
            await client.send_message(message.channel,
                                      'There were no mentions in the past {} messages'
                                      .format(n))

    # *Mods
    if message.content.lower().split()[0] == prefix + "kick":
        if not message.channel.permissions_for(message.author).kick_members:
            await client.send_message(message.channel,
                                      "You don't have permission!")
            return

        if not message.channel.permissions_for(message.author).kick_members:
            await client.send_message(message.channel,
                                      "I don't have permission!")
            return

        if not args:
            await client.send_message(message.channel,
                                      ("No argument! Use {}kick @user "
                                       "`optional reason`"))
            return
        try:
            to_remove = message.server.get_member(
                        re.findall(r'<@!?([0-9]+)>', args[0])[0])
        except IndexError:
            await client.send_message(message.channel, "User not found")
            return

        try:
            await client.kick(to_remove)
        except discord.errors.Forbidden:
            await client.send_message(message.channel, "Could not kick user {}"
                                                       .format(str(to_remove)))
            return

        if len(args) > 1:
            reason = "{0} Kicked: {1}".format(str(to_remove),
                                              await Args(args[1:]).toString())
        else:
            reason = '{0} Kicked: No reason given'.format(str(to_remove))

        await client.send_message(message.channel, reason)

    if message.content.lower().split()[0] == prefix + "ban":
        if not message.channel.permissions_for(message.author).ban_members:
            await client.send_message(message.channel,
                                      "You don't have permission!")
            return

        if not message.channel.permissions_for(message.author).ban_members:
            await client.send_message(message.channel,
                                      "I don't have permission!")
            return

        if not args:
            await client.send_message(message.channel,
                                      ("No argument! Use {}ban @user "
                                       "`optional reason`"))
            return

        try:
            to_remove = message.server.get_member(
                        re.findall(r'<@!?([0-9]+)>', args[0])[0])
        except IndexError:
            await client.send_message(message.channel, "User not found")
            return
        if 'purge=' in message.content.lower():
            for i in args:
                if 'purge=' in i:
                    try:
                        purge = int(i.replace("purge=", ""))
                        end = args.index(i)
                    except ValueError:
                        await client.send_message(message.server,
                                                  "Invalid purge setting")
                        return
        else:
            purge = 0
            end = len(args)

        try:
            await client.ban(to_remove, delete_message_days=purge)
        except discord.errors.Forbidden:
            await client.send_message(message.channel, "Could not ban user {}"
                                                       .format(str(to_remove)))
            return

        if len(args) > 1:
            reason = "{0} Banned: {1}".format(str(to_remove),
                                              await Args(args[1:end]).toString())
        else:
            reason = '{0} Banned: No reason given'.format(str(to_remove))

        await client.send_message(message.channel, reason)

    # *Make this section more user friendly
    if (message.channel.permissions_for(message.author).manage_server
            or message.author.id == '142510125255491584'):
        if message.content.lower().split()[0] == prefix + 'settings':
            if args is None:
                return  # *Show all settings
            else:
                try:
                    await client.send_message(message.channel, bot.settings[message.server.id][args[0]])
                except KeyError:
                    await client.send_message(message.channel,
                                              "Invalid setting argument")
            return

        if message.content.lower().split()[0] == prefix + 'setting':
            if args is None:
                await client.send_message(message.channel,
                                          "Use {}setting info to see what you can set"
                                          .format(prefix))
                return
            try:
                await client.send_message(message.channel, await set(message.server, args[0], await Args(args[1:]).toString()))
            except IndexError:
                await client.send_message(message.channel, await set(message.server, args[0], message.channel))

    if (message.channel.permissions_for(message.author).manage_server or
            message.author.id == '142510125255491584'):
        if message.content.lower().split()[0] == prefix + 'purge':
            deleted = 0
            num = bot.settings[message.server.id]['clear']

            if args:
                if args[0].isdigit():
                    num = int(args[0])
                else:
                    await client.send_message(message.channel, "Invalid argument `{}`. Needs to be a number".format(args[0]))
                    return
            async for log in client.logs_from(message.channel, limit=num):
                if log.author == client.user:
                    await client.delete_message(log)
                    deleted += 1

            if deleted:
                msg = await client.send_message(message.channel,
                                                "Deleted {} of my messages"
                                                 .format(deleted))
                await asyncio.sleep(10)
                await client.delete_message(msg)

        if message.content.lower().split()[0] == prefix + "clear":
            deleted = 0

            try:
                num = int(args[0])
            except ValueError:
                await client.send_message(message.channel, "Invalid arg {}"
                                          .format(args[0]))
                return
            except IndexError:
                num = bot.settings[message.server.id]['clear']
            finally:
                num = 10000 if num > 9999 else num

            if args and len(args) >= 2:
                to_delete = message.server.get_member(
                            re.findall(r'<@!?([0-9]+)>', args[1])[0])
                async for msg in client.logs_from(message.channel, limit=num):
                    if msg.author == to_delete:
                        await client.delete_message(msg)
                        deleted += 1
            else:
                async for msg in client.logs_from(message.channel, limit=num):
                    await client.delete_message(msg)
                    deleted += 1
            if deleted:
                msg = await client.send_message(message.channel,
                                                "{0} has Deleted {1} messages!"
                                                .format(message.author.mention,
                                                        deleted))
                await asyncio.sleep(15)
                await client.delete_message(msg)

    # *Owner
    if message.author.id == '142510125255491584':
        if message.content.lower().split()[0] == prefix + 'blacklist':
            if args:
                await blacklist(args[0])
            else:
                await blacklist(message.server.id)
            await client.send_message(message.channel, ':ok_hand:')

        if message.content.lower().split()[0] == prefix + 'reload':
            await bot.reload_settings()
            await client.send_message(message.channel, "Reloaded")

        if message.content.lower().split()[0] == prefix + "todo":
            if args[0] == "readall":
                with open("todo.txt", "r") as outfile:
                    await client.send_message(message.channel, outfile.read())
                    return
            else:
                with open("todo.txt", "a+") as todofile:
                    print(await args.toString(), file=todofile)
                    return

        if message.content.lower().split()[0] == prefix + "eval":
            python = '```py\n{}\n```'
            cmd = bytes(message.content
                        .replace(prefix + 'eval', "", 1),
                                 "utf-8").decode("unicode_escape")
            try:
                result = eval(cmd)
                if inspect.isawaitable(result):
                    result = await result
            except Exception as e:
                await client.send_message(message.channel,
                                          python.format(type(e).__name__ +
                                                        ': ' + str(e)))
                return

            await client.send_message(message.channel, python.format(result))

        if message.content.lower().split()[0] == prefix + "py":
            python = '```py\n{}\n```'
            cmd = bytes(message.content.replace(prefix+'py', "", 1), "utf-8").decode("unicode_escape").strip()
            try:
                result = exec(cmd)
                if inspect.isawaitable(result):
                    result = await result
            except Exception as e:
                await client.send_message(message.channel,
                                          python.format(type(e).__name__ +
                                                        ': ' + str(e)))
                return
            await client.send_message(message.channel, python.format(result))

        if message.content.lower().split()[0] == prefix + "stop":
            await client.send_message(message.channel, "Hammer Time!")
            await client.logout()

    if message.channel.id in bot.settings[message.server.id]['silent']:
        return

    # *Regex when
    if "ruka" in message.content.lower():
        await client.send_message(message.channel,
                                  "_Did you mean_: {}"
                                  .format(message.content.lower()
                                          .replace("ruka", "Nuka")))

    if 'oshit' in message.content.lower():
        if 'OSHIT' in message.content:
            await client.send_message(message.channel, "WADDUP")
            return

        await client.send_message(message.channel, "waddup")

    if ('cyka' in message.content.lower() and
            'blyat' not in message.content.lower()):
        await client.send_message(message.channel, 'Блять')

    if message.content.lower() == 'kek':
        if not random.randint(0, 100):
            await client.send_message(message.channel,
                                      "Did you know that kek backwards is kek?"
                                      )
        return

    if ('ayy' in message.content.lower() and
            'lmao' not in message.content.lower()):
        await client.send_message(message.channel, "lmao")

    if ('lmao' in message.content.lower() and
            'ayy' not in message.content.lower()):
        await client.send_message(message.channel, "ayy")

    if 'kill all bots' in message.content.lower():
        await client.send_message(message.channel,
                                  "Tracing {}'s IP..."
                                  .format(message.author.mention))
        await asyncio.sleep(5)
        await client.send_message(message.channel, "Ddox beginning..")

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

    if message.content.lower()== ("wew"):
        if "WEW" in message.content:
            await client.send_message(message.channel, "LAD")
            return
        await client.send_message(message.channel, "lad")


@client.event
async def on_member_join(member):
    if member == client.user:
        return

    if not bot.settings[member.server.id]['default_roles']:
        return

    for role in member.server.roles:
        if role.name in bot.settings[member.server.id]['default_roles']:
            try:
                await client.add_roles(member, role)
            except Exception as e:
                await client.send_message(member.server,
                                          ("Unable to give role:{0}"
                                           " to new member {1}")
                                          .format(role.name, str(member)))


@client.event
async def on_server_join(server):
    await client.send_message(discord.Object(id='222828628369604609'),
                              """**Joined {0.name}[id: {0.id}]
Owner:[Name: {0.owner}], [ID: {0.owner.id}]
Members: {0.member_count}
Region: {0.region}
2FA Required: {1}
Verification Level: {0.verification_level}**
Icon: {0.icon_url}"""
                              .format(server, bool(server.mfa_level)))
    if server.id in bot.blacklist:
        client.leave_server(server)
    await create_server(server)


@client.event
async def on_server_remove(server):
    await client.send_message(discord.Object(id='222828628369604609'),
                              "**__Left {}__**".format(server.name))


@client.event
async def on_ready():
    print('------')
    print("Log : {}".format(bot.log_name))
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print("https://discordapp.com/oauth2/authorize?&client_id=" +
          client.user.id + "&scope=bot&permissions=3688992")
    await client.send_message(discord.Object(id='222828628369604609'), "**-------------------**")
    await client.send_message(discord.Object(id='222828628369604609'),
                              "Bot Started")
    await client.send_message(discord.Object(id='222828628369604609'),
                              "Took {} to start"
                              .format(str(datetime.datetime.now() - start)))
    print("Took {} to start".format(str(datetime.datetime.now() - start)))
    print('------')
    for server in client.servers:
        await client.send_message(discord.Object(id='222828628369604609'),
                                  bot.update_server(server))
    await client.send_message(discord.Object(id='222828628369604609'), "**-------------------**")
    await suggest_reset()


print("Starting...")
client.run('token')
