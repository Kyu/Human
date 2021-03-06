# -*- coding: utf-8 -*-
import asyncio
import discord
import yaml
from gingerit.gingerit import GingerIt
import Fun
import Utils
from Utils import Args, StartupErr


import time  # *Switch all time to datetime
from datetime import datetime
import pickle
import random
import os
import subprocess
import inspect
import re

start = datetime.now()


class Bot:
    def __init__(self):
        self.bootup = self.boot()
        self.started = False
        self.name = "Human"
        self.author = '@Yu#9162'
        self.library = 'discord.py'
        self.source = 'https://github.com/Kyu/Human'
        self.invite = "https://discordapp.com/oauth2/authorize?&client_id=210448501748924416&scope=bot&permissions=471198782"
        self.version = 'Beta0.8'
        self.config_name = 'config.yml'
        self.start = datetime.now()
        self.commandsrun = 0
        self.lastsaid = {}
        self.defaultprefix = "."  # *Find something better
        self.setting_format = {"prefix": ".", "clear": 100, "silent": [],
                               "disabled": [], "default_roles": [],
                               "disabled_commands": [], "mod_log": ""}
        self.TIME_FORMAT = "%H:%M:%S"
        self.DATE_FORMAT = '%Y-%m-%d'
        self.log_name = self.start.strftime('%Y-%m-%d-%H-%M-%S') + ".log"
        self.log_dir = os.getcwd() + "/logs/" + self.log_name
        self.commands = ('purge', 'blacklist', 'reload', 'say', 'roll', 'c', 'flip', 'play', 'clear', 'py', 'stop', '8ball', 'stats',
                         'whosaid', 'case', 'reverse', 'settings', 'setting', 'grammar', 'meow', 'doggo', 'dog', 'puppy', 'kitty', 'kitten',
                         'ping', 'g', 'mentions', 'mention', 'mentioned', 'info', 'invite', 'kick', 'ban', 'suggest', 'wiki', 'wikipedia',
                         'xkcd', 'shell', 'set', 'suggestion')
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
            with open(self.config_name, "w", encoding='utf-8') as cfg:
                yaml.dump(sess, cfg, default_flow_style=False)
            self.settings = sess
        else:
            raise StartupErr("Something is wrong with your config")
        self.blacklist = self.settings['blacklist']

        return True

    def update_server(self, server):
        settings = {"prefix": self.defaultprefix, "clear": 100, "silent": [],
                    "disabled": [], "default_roles": [],
                    "disabled_commands": [], "mod_log": "", "name": server.name}

        updated = []

        for i in settings:
            if i not in self.settings[server.id]:
                self.settings[server.id][i] = settings[i]
                updated.append(i)

        self.reload_settings()

        if updated:
            return "Updated: {0} in {1.name}".format(", ".join(updated), server)
        else:
            return "Nothing to update in {0.name}".format(server)

    def reload_settings(self):
        with open(self.config_name, "w", encoding='utf-8') as cfg:
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

Key:
<>: Required argument
[]: Optional argument
||: Alias to a command

__**Level 0: Normal users**__
Repeat after me: {0}say <thing>
See who last used {0}say: {0}whosaid
Chatbot: {0}c <message>
Roll a die: {0}roll [number of sides]
Flip a coin: {0}flip
Radio: {0}play <URL>
Magic 8-ball:{0}8ball [query]
Stats: {0}stats
Bot info: {0}info
New Quote: {0}case <thing> <quote>
View a quote:tell me about <thing>
Reverse a sentence: {0}reverse <thing>
See past mentions: {0}mentions [number]
Grammar checker: {0}grammar <thing> |{0}g
Invite link: {0}invite
Wikipedia article: {0}wiki <query> [max sentences] | {0}wikipedia
xkcd comic: {0}xkcd [number, random]
Random Kitty: {0}kitty


__**Level 0: Server Mods**__
Clear chat: {0}clear [optional number, default is 100] [@ user]
View Settings: {0}settings [clear, silent, disabled, prefix]
Change a setting: {0}set <setting name> <value> | Do `{0}setting info` to view what you settings can change
Send a suggestion: {0}suggestion <suggestion>
Kick a user: {0}kick <@User/userid> [reason]
Ban a user: {0}kick <@User/userid> [reason] [purge=n]

Bot Discord:
https://discord.gg/2MqkeeJ
'''
# add the .format() here


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


def getDoggo():
    doggo = 'random.dog/ doggo'
    return doggo


def getKitty():
    kitty = 'random.cat/ kitty'
    return kitty


async def save_convo(obj):
    with open('convos.pk1', 'wb') as output:
        pickle.dump(dict(obj), output, -1)
    return


async def send_feedback(message, type, input=False):
    input = message.content if not input else input
    embed = discord.Embed(description="")
    embed.color = discord.Colour.blue() if type == "Suggestion" else discord.Colour.orange()
    embed.set_author(name=message.author, icon_url=message.author.avatar_url)
    if message.server:
        embed.add_field(name=message.server.name, value=message.server.id)
        embed.add_field(name=message.channel.name, value=message.channel.id)
    embed.timestamp = message.timestamp
    embed.add_field(name=type, value=input, inline=False)
    await client.send_message(discord.Object(id='240528124297740298'), embed=embed)


async def bot_chat(channel, chatters=2):
    prompt = "Hi"
    prefixes = [":speech_balloon:", ":thought_balloon:", ":cloud_lightning:", ":diamond_shape_with_a_dot_inside:", ":thinking:",
                ":sunglasses:", ":poop:", ":eye_in_speech_bubble:", ":speech_left:", ":eyes:", ":robot:", ":no_mouth:", ":globe_with_meridians:",
                ":capital_abcd:", ":interrobang:"]

    if chatters > len(prefixes):
        return "Too much bots. Max is {}".format(len(prefixes))

    while bot.allow_convos[channel.id]:
        for i in range(1, chatters + 1):
            pr = "{0}Chatter: {1}".format(channel.id, i)
            c = Fun.convo_manager(pr)
            prompt = c.ask(prompt)
            await client.send_message(channel, "{0} {1}".format(prefixes[i], prompt))
            await asyncio.sleep(3)

        await save_convo(bot.convos)

    return "Convo Done"


# *Log better
async def take_log(message):
    # logdir = os.getcwd() + "/logs/"

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


async def stats():
    uptime = str(datetime.now() - bot.start).split(".")[0]
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
             "mod_log": "Channel where the bot logs mod actions"}  # "bot_commanders": "Users able to do bot level commands"} #convert to str

    if case == 'info' or case == 'help':
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
            except Exception:
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
        if (case == 'default_roles' or case == 'disabled_commands'):
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
    with open(bot.config_name, "w", encoding='utf-8') as cfg:
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
    # default_cfg[server.id]['name'] = server.name

    with open(cfg_name, 'r') as f:
        config = yaml.load(f)

    try:
        if server.id in list(config):
            return

        with open(cfg_name, "a", encoding='utf-8') as cfg:
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

    with open("config.yml", "w", encoding='utf-8') as f:
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
        if message.server.id not in bot.settings:
            await create_server(message.server)

        prefix = bot.settings[message.server.id]['prefix']

    if message.author == client.user:
        if message.channel.is_private:
            if message.content.startswith("Here are your commands!"):
                return
        await take_log(message)

    if message.author.bot:
        return

    for i in bot.commands:
        if message.content.lower().split()[0] == prefix + i:
            if message.channel.is_private and i != "help":
                return
            if i in bot.settings[message.server.id]["disabled_commands"] and (not i.startswith("set")):
                return
            if (message.channel.id in bot.settings[message.server.id]['disabled']) and (not i.startswith('set')):
                return
            args = (Args(message.content.split()[1:])
                    if message.content.split()[1:] else None)
            bot.commandsrun += 1
            await take_log(message)

    # *Triggers
    if (message.content == client.user.mention or
            message.content == (client.user.mention + " help") or
            message.content.lower().split()[0] == prefix + 'help'):
        await client.send_message(message.author,
                                  bot.helpText().format(prefix, message.server))
        await client.send_message(message.channel,
                                  "Help Sent to {}!".format(message.author.mention))

    if client.user.mention in message.content:
        await take_log(message)

    if message.content.lower().split()[0] == prefix + '8ball':
        if not args:
            await client.send_message(message.channel,
                                      "Actually there are only 7 dragon balls")
            return
        await client.send_message(message.channel, Fun.fortune())

    if message.content.lower().split()[0] == prefix + 'say':
        if args is None:
            return
        await sent_from(message.channel.id, message.author)
        await client.send_message(message.channel,
                                  message.content.replace(prefix + "say", "", 1
                                                          ))

    if message.content.lower().split()[0] == prefix + 'reverse':
        await client.send_message(message.channel,
                                  '\u202e{}'.format(args.toString()))

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
                                        .format(args.toString()))

        corrected = await correctGrammar(args.toString())

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
            c = Fun.convo_manager(message.author)
            await client.send_message(message.channel,
                                      c.ask(args.toString()))
            await save_convo(bot.convos)
        except UnicodeEncodeError as e:
            await client.send_message(message.channel,
                                      "I don't really like emoji atm")
        except ConnectionError:
            await client.send_message(message.channel,
                                      (":x: Oops something went wrong! "
                                       "Is the bot server down?"))

    # *Useful
    if message.content.lower().split()[0] == prefix + "invite":
        await client.send_message(message.channel, bot.invite)

    if message.content.lower().split()[0] == prefix + 'info':
        await client.send_message(message.channel, bot.info())

    if message.content.lower().split()[0] == prefix + 'ping':
        pong = await client.send_message(message.channel, ":ping_pong:")
        ping = pong.timestamp - message.timestamp
        await client.edit_message(pong,
                                  "Response took {}s"
                                  .format((str(ping).split(':')[2])
                                          .strip('0')))

    if message.content.lower().split()[0] == prefix + "suggestion" or message.content.lower().split()[0] == prefix + "suggest":
        if not args:
            await client.send_message(message.channel, ("Do nothing is a great suggestion. "
                                                        "I'll do that all day"))
            return

        try:
            if bot.suggest_timeout[message.author.id] >= 5:
                await client.send_message(message.channel,
                                          "Enough suggestions for today {}."
                                          .format(message.author.mention))
                return
        except KeyError:
            bot.suggest_timeout[message.author.id] = 0

        bot.suggest_timeout[message.author.id] += 1
        await send_feedback(message, "Suggestion", input=args.toString() + "\n")

    if (message.content.lower().split()[0] == prefix + 'cat' or
            message.content.lower().split()[0] == prefix + 'meow' or
            message.content.lower().split()[0] == prefix + 'kitten' or
            message.content.lower().split()[0] == prefix + 'kitty'):
        await client.send_message(message.channel, await Fun.get_kitty())

    if (message.content.lower().split()[0] == prefix + 'pupper' or
            message.content.lower().split()[0] == prefix + 'doggo' or
            message.content.lower().split()[0] == prefix + 'dog' or
            message.content.lower().split()[0] == prefix + 'puppy'):
        await client.send_message(message.channel, getDoggo())

    # *Finish this
    if message.content.lower().split()[0] == prefix + "urban":
        if not len(message.content.split()) >= 2:
            await client.send_message(message.channel, "Word?")
            return
        # *parse json from http://api.urbandictionary.com/v0/define?term= + " ".join(message.content.split()[1:])

    if (message.content.lower().split()[0] == prefix + "wiki" or
            message.content.lower().split()[0] == prefix + "wikipedia"):
        if not args:
            await client.send_message(message.channel, "Query must not be empty!")
            return

        sentences = 3

        if args[-1].isdigit():
            sentences = int(args[-1]) if int(args[-1]) > 0 and int(args[-1]) < 11 else 3
        if len(args) < 2:
            args.append(args[0])
        await client.send_message(message.channel, Fun.wiki(args(args[:-1]).toString(), sentences=sentences))

    if message.content.lower().split()[0] == prefix + "xkcd":
        # Do explain later, too lazy rn
        if not args:
            comic = Fun.get_xkcd()
        elif args[0] == "random":
            comic = Fun.get_xkcd(random=True)
        elif args[0].isdigit():
            comic = Fun.get_xkcd(number=int(args[0]))
        else:
            comic = Fun.get_xkcd()

        await client.send_message(message.channel, comic[0])
        await client.send_message(message.channel, comic[1])
        return
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
            to_remove = message.server.get_member(re.findall(r'<@!?([0-9]+)>', args[0])[0])
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
                                              args(args[1:]).toString())
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
            to_remove = message.server.get_member(re.findall(r'<@!?([0-9]+)>', args[0])[0])
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
                                              args(args[1:end]).toString())
        else:
            reason = '{0} Banned: No reason given'.format(str(to_remove))

        await client.send_message(message.channel, reason)

    # *Make this section more user friendly
    if (message.channel.permissions_for(message.author).manage_server or message.author.id == '142510125255491584'):
        if message.content.lower().split()[0] == prefix + 'settings':
            if args is None:
                await client.send_message(message.channel, await set(message.server, "view", args(args[1:]).toString()))
            elif args[0] == "info" or args[0] == "help":
                await client.send_message(message.channel, await set(message.server, args[0], args(args[1:]).toString()))
            else:
                try:
                    await client.send_message(message.channel, bot.settings[message.server.id][args[0]])
                except KeyError:
                    await client.send_message(message.channel,
                                              "Invalid setting argument")
            return

        if message.content.lower().split()[0] == prefix + 'set':
            if args is None:
                await client.send_message(message.channel,
                                          "Use {}settings help to see what you can set"
                                          .format(prefix))
                return
            _set = args(args[1:]).toString()

            try:
                if _set:
                    await client.send_message(message.channel, await set(message.server, args[0], args(args[1:]).toString()))
                else:
                    await client.send_message(message.channel, await set(message.server, args[0], message.channel))
            except Exception as e:
                print(type(e).__name__ + ': ' + str(e))

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
                msg = await client.send_message(message.channel, "Deleted {} of my messages".format(deleted))
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
            except TypeError:
                num = bot.settings[message.server.id]['clear']

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
                    print(args.toString(), file=todofile)
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
            result = str(result)
            end = [result[i:i+1900] for i in range(0, len(result), 1900)]
            for i in end:
                await client.send_message(message.channel, python.format(i))

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
            result = str(result)
            end = [result[i:i+1900] for i in range(0, len(result), 1900)]
            for i in end:
                await client.send_message(message.channel, python.format(i))

        if message.content.lower().split()[0] == prefix + "shell":
            python = '```py\n{}\n```'
            cmd = bytes(message.content.replace(prefix+'shell', "", 1), "utf-8").decode("unicode_escape").strip()
            try:
                result = subprocess.getoutput(cmd)
            except Exception as e:
                await client.send_message(message.channel,
                                          python.format(type(e).__name__ +
                                                        ': ' + str(e)))
                return

            result = str(result)
            end = [result[i:i + 1900] for i in range(0, len(result), 1900)]
            for i in end:
                await client.send_message(message.channel, python.format(i))

        if message.content.lower().split()[0] == prefix + "stop":
            await client.send_message(message.channel, "Hammer Time!")
            await client.logout()

    if message.channel.is_private or message.channel.id in bot.settings[message.server.id]['silent']:
        return

    # *Regex when
    if message.content.lower() == "cyka":
        await client.send_message(message.channel, 'Блять')

    if message.content.lower() == 'kek':
        if not random.randint(0, 100):
            await client.send_message(message.channel,
                                      "Did you know that kek backwards is kek?"
                                      )
    return

    if 'kill all bots' in message.content.lower():
        await client.send_message(message.channel,
                                  "Tracing {}'s IP..."
                                  .format(message.author.mention))
        await asyncio.sleep(5)
        await client.send_message(message.channel, "Ddox beginning..")

    if message.content.lower() == '/o/':
        await client.send_message(message.channel, "\\o\\")

    if message.content.lower() == '\\o\\':
        await client.send_message(message.channel, "/o/")

    if message.content.lower() == '/o\\':
        await client.send_message(message.channel, '\\o/')

    if message.content.lower() == '\\o/':
        await client.send_message(message.channel, '/o\\')

    if message.content.lower().startswith("good boy"):
        await client.send_message(message.channel, "Thanks!")

    if message.content.lower() == "wew":
        if "WEW" in message.content:
            await client.send_message(message.channel, "LAD")
            return
        await client.send_message(message.channel, "lad")


@client.event
async def on_member_join(member):
    if member == client.user:
        return
    if member.bot:
        return

    if not bot.settings[member.server.id]['default_roles']:
        return
    if member.bot:
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
    if member.server.id == "246969937271324672":
        await bot.change_nickname(member, "Comrade {0.name}".format(member))


@client.event
async def on_server_join(server):
    if server.id in bot.blacklist:
        client.leave_server(server)
    await create_server(server)

    check = Utils.check_bot_server(server)
    bot_server = True if check >= 75 else False
    check = str(check) + "%"
    emb = discord.Embed(title="")
    emb.description = ":warning: " + check if bot_server else check
    emb.color = discord.Colour.green()
    emb.set_author(name=server.owner)
    emb.set_thumbnail(url=server.owner.avatar_url)
    emb.add_field(name=server.name, value=server.id, inline=True)
    emb.add_field(name="Owner", value=server.owner.id, inline=True)
    emb.add_field(name="Members", value=server.member_count, inline=False)
    emb.set_image(url=server.icon_url) if server.icon_url else None

    await client.send_message(discord.Object(id='222828628369604609'), embed=emb)
    # .format(bot.settings[server.id]['prefix'])
    await client.send_message(server, ("Thanks for inviting me to your server! Mention me or use .help for help.\n"
                                       "You can also change the server's prefix using .setting prefix {newprefix}"
                                       "You can also join https://discord.gg/2MqkeeJ for updates and to talk with the creator.\n"
                                       "Make sure to use .suggestion to give feedback on your experience with the bot!"))


@client.event
async def on_server_remove(server):
    emb = discord.Embed()
    emb.color = discord.Colour.red()
    emb.add_field(name=server.name, value=server.id, inline=True)
    await client.send_message(discord.Object(id='222828628369604609'), embed=emb)

    await client.send_message(server.owner, ("I have been removed from {}. "
                                             "Do you have any feedback to give on your experience with the bot"
                                             "(suggestions, improvements?). If so, type it here and the creator will recieve it. This message expires in 2 hours").format(server.name))
    resp = await client.wait_for_message(timeout=7200, author=server.owner)
    if not resp.content:
        return
    else:
        await send_feedback(resp, "Feedback")


@client.event
async def on_ready():
    print('------')
    print("Log : {}".format(bot.log_name))
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print("https://discordapp.com/oauth2/authorize?&client_id=" +
          client.user.id + "&scope=bot&permissions=3688992")
    if not bot.started:
        await client.send_message(discord.Object(id='251408655998517249'), "**-----**")
        await client.send_message(discord.Object(id='251408655998517249'), "Bot Started")
        await client.send_message(discord.Object(id='251408655998517249'),
                                  "Took {} to start"
                                  .format(str(datetime.now() - start)))
        print("Took {} to start".format(str(datetime.now() - start)))
        print('------')
        updates = []
        updated = 0
        for server in client.servers:
            await create_server(server)
        for server in client.servers:
            updates.append(bot.update_server(server))
        for update in updates:
            if not update.startswith("Nothing to update"):
                await client.send_message(discord.Object(id='251408655998517249'), update)
                updated += 1
        if not updates:
            await client.send_message(discord.Object(id='251408655998517249'), "All servers have up to date configs")
        else:
            await client.send_message(discord.Object(id='251408655998517249'), "Updated {} configs".format(updated))
        await client.send_message(discord.Object(id='251408655998517249'), "**-----**")
        await client.loop.create_task(suggest_reset())
        bot.started = True
    else:
        await client.send_message(discord.Object(id='251408655998517249'), "Reconnected")

if __name__ == "__main__":
    Fun.bot = bot
    print("Starting...")
    client.run('bloop')
