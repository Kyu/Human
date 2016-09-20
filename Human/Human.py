import asyncio
import discord
from cleverbot import Cleverbot
from bs4 import BeautifulSoup
import markovify
import yaml
from gingerit.gingerit import GingerIt


import time  # *Switch all time to datetime
import datetime
import pickle
import random
import os
from urllib.request import Request, urlopen
import traceback


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
        self.version = 'Beta0.4'
        self.config_name = 'config.yml'
        self.start = datetime.datetime.now()
        self.commandsrun = 0
        self.lastsaid = {}
        self.defaultprefix = "."  # *Find something better
        self.TIME_FORMAT = "%H:%M:%S"
        self.DATE_FORMAT = '%Y-%m-%d'
        self.log_name = self.start.strftime('%Y-%m-%d-%H-%M-%S')
        self.commands = ('purge', 'blacklist', 'reload', 'say', 'roll', 'c',
                         'flip', 'play', 'clear', 'py', 'stop',
                         'todo', 'bloc', 'suggestion', '8ball', 'stats',
                         'whosaid', 'case', 'reverse', 'settings', 'setting',
                         'country', 'eval', 'grammar', 'meow', 'doggo', 'dog',
                         'puppy', 'kitty', 'kitten')
        self.suggest_timeout = {}
        self.loadConvos()
        self.loadSettings()
        # *Add disabled cmds setting

    def boot(self):
        files = ['config.yml', 'todo.txt', 'convos.pk1']
        for file in files:
            if not os.path.exists(file):
                open(file, 'w').close()
        try:
            os.makedirs('logs')
        except OSError:
            if os.path.exists('logs'):
                pass
            else:
                raise

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

    def helpText(self):
        return '''
            Here are your commands!
            The prefix for this server is `{0}`

            __**Level 0: Normal users**__
            Repeat after me: {0}say `thing`
            See who last used {0}say: {0}whosaid
            Chatbot: {0}c `message`
            Country info: {0}country <args>`[info, land, QOL, econ, loc, army]`
            Roll a die: {0}roll `<optional number of sides>`
            Flip a coin: {0}flip
            Radio: {0}play `URL`
            Magic 8-ball:{0}8ball `query`
            BlocSimulator: {0}bloc
            Stats: {0}stats
            New Quote: {0}case `thing`
            Reverse a sentence: {0}reverse `sentence`
            View a quote: {0}case `thing` |also comes with [tell me about] `thing`|



            __**Level 0: Server Mods**__
            ChangeCommandPrefixes: {0}setprefix `newprefix`
            Clear chat: {0}clear `<optional number, default is 1000>`
            View Settings: {0}settings `optional arg[clear, silent, disabled, prefix]`
            Change a setting: {0}setting `setting name` `value` | Do {0}setting `info` to view what you settings can change
            Send a suggestion: {0}suggestion `suggestion`
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


# *Log better
async def take_log(message):
    logdir = os.getcwd() + "\\logs\\"

    try:
        if message.channel.is_private:
            with open(logdir + bot.log_name + ".log", "a+", encoding='utf-8') as text_file:
                print("[{0}] Private Message: {1} : ' {2} ' ".format(time.strftime(bot.TIME_FORMAT, time.localtime()), message.author.name, message.content), file=text_file)

            print("[{0}] Private Message: {1} : ' {2} ' ".format(time.strftime(bot.TIME_FORMAT, time.localtime()), message.author.name, message.content))

        else:
            with open(logdir + bot.log_name + ".log", "a+", encoding='utf-8') as text_file:
                print("[{0}] {1} in  {2}:{3}: '{4}".format(time.strftime(bot.TIME_FORMAT, time.localtime()), message.author.name, message.channel.server.name, message.channel.name, message.content), file=text_file)
            print("[{0}] {1} in  {2}:{3}: '{4}'".format(time.strftime(bot.TIME_FORMAT, time.localtime()), message.author.name, message.channel.server.name, message.channel.name, message.content))
    except UnicodeEncodeError:
        with open(logdir + bot.log_name + ".log", "a+", encoding='utf-8') as text_file:
                print("[{0}] Private Message: {1} : ' {2} ' ".format(time.strftime(bot.TIME_FORMAT, time.localtime()), message.author.id, message.content), file=text_file)


async def get_nation(url, arg):
    '''if url == "args":
        return `info, land, qol, econ, rep, army`
    '''

    NATION_ARGS = {"info": 0, "land": 1, "qol": 2, "econ": 3, "rep": 4,
                   "army": 5}

    if arg == "" or arg not in NATION_ARGS:
        return "**Specify with one of the following arguements <info, land, qol, econ, rep, army>**"
    try:
        req = Request(url, headers={'User-Agent': 'DiscordBot-Human'})
        open_country = urlopen(req).read()
        soup = BeautifulSoup(open_country, "html.parser")
        table = soup.find_all("table", attrs={"class": "table table-striped table-condensed table-hover table-bordered"})
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

        return super_clean_table.replace("\n\n", "\n") + "\n" + "http://www.blocgame.com" + war_country

    return super_clean_table.replace("\n\n", "\n")


async def bloc_speaks():
    try:
        with open(os.path.dirname(os.getcwd()) + '/CelloBoy/BlocSpeaks.txt', 'r',
                                                 encoding='utf-8') as f:
            text = f.read()
    except:
        # Only here because this depends on a file only I have
        return
    text_model = markovify.Text(text)  # *, state_size=4)
    try:
        '''
        if prompt:
            sentence = text_model.make_sentence_with_start(tuple(prompt))
            return sentence
        else:
        '''
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
             'disabled': 'Channels where the bot doesn\'t talk at all'}

    if case == 'info':
        if type(rule) is str:
            return cases[rule]
        else:
            return "You can check for {}".format(", ".join(cases))

    if rule is None:
        return "You need to enter what you want the setting to be changed to!"

    with open(bot.config_name, 'r') as f:
        config = yaml.load(f)

    if server.id in config:
        if case == 'prefix':
            if type(rule) is str:
                config[server.id][case] = rule
            else:
                return "Enter a String"
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
                    what = 'removed from'
                else:
                    config[server.id][case].append(rule)
                    what = 'added to'
            else:
                return "Invalid rule {}".format(rule)
    else:
        await create_server(server)
        case = 'create'
        return "Server rules have just been created. Do {}settings to view them".format(bot.defaultprefix)
    with open(bot.config_name, "w") as cfg:
        yaml.dump(config, cfg, default_flow_style=False)
        bot.loadSettings()

    if case == 'prefix':
        return "Prefix set to {}".format(bot.settings[server.id][case])
    if case == 'clear':
        return "Clear amount set to {}".format(bot.settings[server.id][case])
    return '{0} {1} {2}list'.format(rule, what, case)

async def create_server(server):
    cfg_name = 'config.yml'
    default_cfg = {server.id: {"prefix": bot.defaultprefix, "clear": 100, 'silent': [], 'disabled': []}}

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
        print(e)


async def updatee():
    return 1 + 1


async def update_prefix(server, prefix):
    with open("config.yml") as f:
        list_doc = yaml.load(f)

    if list_doc[server.id]:
        list_doc[server.id]['prefix'] = prefix
    else:
        await create_server(server)
        await update_prefix(server, prefix)

    with open("config.yml", "w") as f:
        yaml.dump(list_doc, f, default_flow_style=False)


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
    if message.channel.id != '142510428591882241':
        return
    if message.author.id in bot.blacklist:
        return
    if message.server.id in bot.blacklist:
        return
    if message.server.id not in bot.settings:
        await create_server(message.server)
    if message.channel.id in bot.settings[message.server.id]['disabled']:
        return

    if message.author.bot:
        return

    if not message.channel.is_private:
        prefix = bot.settings[message.server.id]['prefix']
    else:
        prefix = bot.defaultprefix

    for i in bot.commands:
        if message.content.startswith(prefix + i):
            args = Args(message.content.split()[1:]) if message.content.split()[1:] else None
            bot.commandsrun += 1
            await take_log(message)

    if message.author == client.user:
        if message.content.count('\n') >= 10 and not message.channel.is_private:
            temp_msg = message
            warn_msg = await client.send_message(message.channel, "^ That message will be deleted in 100s for being too long. This is an experimental feature as not to clog chat")
            await asyncio.sleep(100)
            await client.delete_message(warn_msg)
            await client.delete_message(temp_msg)
        return

    if message.content.lower().startswith(prefix + "stop"):
        if message.author.discriminator == "9162":
            await client.send_message(message.channel, "Hammer Time!")
            await client.logout()

    # *Triggers
    if message.content == client.user.mention:
        print(message.author.name + " mentioned you!")
        await client.send_message(message.author, await bot.helptext().format(prefix))

    if client.user.mention in message.content:
        await take_log(message)

    if message.content.startswith(prefix + "8ball"):
        if not args:
            await client.send_message(message.channel, "Actually there are only 7 dragon balls")
            return
        await client.send_message(message.channel, await fortune())

    if message.content.lower().startswith(prefix + "say "):
        await sent_from(message.channel.id, message.author)
        await client.send_message(message.channel, bytes(message.content.replace(prefix+'say', "", 1), "utf-8").decode("unicode_escape"))

    if message.content.lower().startswith(prefix + 'reverse'):
        await client.send_message(message.channel, '\u202e{}'.format(await args.toString()))

    if message.content.lower().startswith(prefix + "whosaid"):
        await client.send_message(message.channel, await who_said(message.channel.id))

    if message.content.lower().startswith(prefix + "flip"):
        if random.choice([0, 1]):
            await client.send_message(message.channel, "You flipped for Heads!")
        else:
            await client.send_message(message.channel, "You flipped for Tails!")

    if message.content.lower().startswith(prefix + 'grammar'):
        msg = await client.send_message(message.channel, "*{}*".format(await args.toString()))
        corrected = await correctGrammar(await args.toString())
        await client.edit_message(msg, "*{0}* :arrow_right: **{1}**".format(msg.content, corrected['result']))

    # *Add text randomnisation
    # *remove max, change message
    if message.content.lower().startswith(prefix + "roll"):
        roll = 6
        if args:
            try:
                if int(args[0]) >= 1:
                    roll = 120 if int(args[0]) >= 120 else int(args[0])
            except ValueError:
                await client.send_message(message.channel, " I said **_number of sides_**\nDo you even know what a number is {}?".format(message.author.mention))
                return
        await client.send_message(message.channel, "Rolled a {0}".format(random.randint(1, roll)))

    if message.content.lower().startswith(prefix + "c "):
        await client.send_typing(message.channel)
        try:
            c = await convo_manager(message.author)
            await client.send_message(message.channel, c.ask(await args.toString()))
            await save_convo(bot.convos)
        except UnicodeEncodeError as e:
            await client.send_message(message.channel, "I don't really like emoji atm")
        except ConnectionError:
            await client.send_message(message.channel, ":x: Oops something went wrong! Is the bot server down?")

    if message.content.lower().startswith(prefix + "bloc"):
        # *prompt = ""
        # if args:
            # prompt = await stringify(args)
        await client.send_message(message.channel, await bloc_speaks())

    # *Useful
    if message.content.lower().startswith(prefix + "help"):
        await client.send_message(message.author, await bot.helptext().format(prefix))

    if message.content.lower().startswith(prefix + "suggestion"):
        if not args:
            await client.send_message(message.channel, "Do nothing is a great suggestion. I'll do that all day")
            return

        try:
            if bot.suggest_timeout[message.author.id] >= 5:
                await client.send_message(message.channel, "Enough suggestions for today {}.".format(message.author.mention))
                return
        except KeyError:
            bot.suggest_timeout[message.author.id] = 1

        bot.suggest_timeout[message.author.id] += 1
        with open("todo.txt", "a") as todofile:
            print("[Suggestion from]{0}: {1}".format(message.author.name, await args.toString()), file=todofile)

    if message.content.lower().startswith(prefix + 'cat') or message.content.lower().startswith(prefix + 'meow') or message.content.lower().startswith(prefix + 'kitten') or message.content.lower().startswith(prefix + 'kitty'):
        await client.send_message(message.channel, await getKitty())

    if message.content.lower().startswith(prefix + 'pupper') or message.content.lower().startswith(prefix + 'doggo') or message.content.lower().startswith(prefix + 'dog') or message.content.lower().startswith(prefix + 'puppy'):
        await client.send_message(message.channel, await getDoggo())

    # *Finish this
    if message.content.lower().startswith(prefix + "urban "):
        if not len(message.content.split()) >= 2:
            await client.send_message(message.channel, "Word?")
            return
        # *parse json from http://api.urbandictionary.com/v0/define?term= + " ".join(message.content.split()[1:])

    if message.content.lower().startswith(prefix + "country "):
        if args:
            m = args[0]
            try:
                args[1]
            except IndexError:
                await client.send_message(message.channel, "Specify with an arguement `<info, land, qol, econ, rep, army>`" )
                return
        else:
            await client.send_message(message.channel, "I need a country url here")
            return

        try:
            if m.isdigit():
                fullm = "http://blocgame.com/stats.php?id=" + m
                info = await get_nation(fullm, args[1])
                await client.send_message(message.channel, "Getting info from http://blocgame.com/stats.php?id=" + m + "\n" +info)
            elif "blocgame.com/stats.php?id=" in m:
                info = await get_nation(m, args[1])
                await client.send_message(message.channel, "Getting info from "+ m + "\n" + info)
            else:
                await client.send_message(message.channel, "Bad nation link/number")
        except IndexError:
            await client.send_message(message.channel, "That nation does not exist")

    if message.content.lower().startswith(prefix + "play "):
        await client.send_message(message.server, ":x:Disabled due to bandwith issues")

    if message.content.lower().startswith(prefix + "stats"):
        await client.send_message(message.channel, await stats())

    # *Mods
    if message.content.lower().startswith(prefix + "kick"):
        if not message.channel.permissions_for(message.author).kick_members:
            await client.send_message(message.channel, "You don't have permission!")
            return

        if not message.channel.permissions_for(message.author).kick_members:
            await client.send_message(message.channel, "I don't have permission!")
            return

        if not args:
            await client.send_message(message.channel, "No argument!")
            return

        #await client.kick(user.mentioned_in(message))

        if len(message.content.split()) > 1:
            reason = message.author.name + "Kicked you for: " + " ".join(message.content.split()[2:])
        else:
            reason = ""

        for i in args:
            await client.send_message(message.channel, i)

    # *Make this section more user friendly
    if message.content.lower().startswith(prefix + 'settings'):
        if not message.channel.permissions_for(message.author).manage_server:
            await client.send_message(message.channel, "You do not have permission to do this!")
            return
        if args is None:
            pass  # *Show all settings
        else:
            try:
                await client.send_message(message.channel, bot.settings[message.server.id][args[0]])
            except KeyError:
                await client.send_message(message.channel, "Invalid setting argument")
        return

    if message.content.lower().startswith(prefix + 'setting'):
        if not message.channel.permissions_for(message.author).manage_server:
            await client.send_message(message.channel, "You do not have permission to do this!")
            return
        if args is None:
            await client.send_message(message.server, "Use {}settings info to see what you can set".format(prefix))
            return
        try:
            await client.send_message(message.channel, await set(message.server, args[0], args[1]))
        except IndexError:
            await client.send_message(message.channel, await set(message.server, args[0], message.channel))

    if message.content.lower().startswith(prefix + "setprefix "):
        if not message.channel.permissions_for(message.author).manage_server:
            await client.send_message(message.channel, "You do not have permission to do this!")
            return

        await update_prefix(message.server, args[0])
        await client.send_message(message.channel, "New prefix set: " + bot.settings[message.server.id]['prefix'])

    if message.content.lower().startswith(prefix + 'purge'):
        if not message.channel.permissions_for(message.author).manage_server:
            if message.author.id != '142510125255491584':
                await client.send_message(message.channel, "No permission!")
                return

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

    if message.content.lower().startswith(prefix + "clear"):
        if not message.channel.permissions_for(message.author).manage_server:
            if message.author.id != '142510125255491584':
                await client.send_message(message.channel, "No permission!")
                return

        deleted = 0
        num = bot.settings[message.server.id]['clear']
        try:
            if args:
                if args[0].isdigit():
                    num = int(args[0])
                else:
                    await client.send_message(message.channel, "Invalid argument `{}`. Needs to be a number".format(args[0]))
                    return
            async for log in client.logs_from(message.channel, limit=num):
                await client.delete_message(log)
                deleted += 1
        except discord.errors.Forbidden:
            await client.send_message(message.channel, "I don't have permission to do this. Use {}purge instead?".format(prefix))

        if deleted:
            msg = await client.send_message(message.channel, "{0} has Deleted {1} messages!".format(message.author.mention, deleted))
            await asyncio.sleep(10)
            await client.delete_message(msg)

    # *Owner
    if message.author.id == '142510125255491584':
        if message.content.lower().startswith(prefix + 'blacklist'):
            if message.author.id == '142510125255491584':
                if args:
                    await blacklist(args[0])
                else:
                    await blacklist(message.server.id)
                await client.send_message(message.channel, ':ok_hand:')

        if message.content.lower().startswith(prefix + 'reload'):
            if message.author.id == '142510125255491584':
                bot.loadSettings()
                await client.send_message(message.channel, "Reloaded")

        if message.content.lower().startswith(prefix + "todo "):
            if message.author.discriminator == "9162":
                if args[0] == "readall":
                    with open("todo.txt", "r") as outfile:
                        await client.send_message(message.channel, outfile.read())
                        return
                else:
                    with open("todo.txt", "a+") as todofile:
                        print(await args.toString(), file=todofile)
                        return

        if message.content.lower().startswith(prefix + "eval "):
            if message.author.discriminator == "9162":
                cmd = bytes(message.content.replace(prefix+'eval', "", 1), "utf-8").decode("unicode_escape")
                try:
                    await client.send_message(message.channel, eval(cmd))
                    await client.send_message(message.channel, "Done")
                except:
                    await client.send_message(message.channel, traceback.format_exc().replace('Guest', 'Me'))
                    return

        if message.content.lower().startswith(prefix + "py "):
            if message.author.discriminator == "9162":
                cmd = bytes(message.content.replace(prefix+'py', "", 1), "utf-8").decode("unicode_escape").strip()
                try:
                    await client.send_message(message.channel, exec(cmd))
                    await client.send_message(message.channel, ":ok_hand:")
                except:
                    await client.send_message(message.channel, traceback.format_exc().replace('Guest', 'Me'))
                    return

        if message.content.lower().startswith(prefix + "stop"):
            if message.author.discriminator == "9162":
                await client.send_message(message.channel, "Hammer Time!")
                await client.logout()

    if message.channel.id in bot.settings[message.server.id]['silent']:
        return

    # *Regex when
    if "ruka" in message.content.lower():
        await client.send_message(message.channel, "_Did you mean_: {}".format(message.content.lower().replace("ruka", "Nuka")))

    if 'oshit' in message.content.lower():
        if 'OSHIT' in message.content:
            await client.send_message(message.channel, "WADDUP")
            return

        await client.send_message(message.channel, "waddup")

    if 'cyka' in message.content.lower() and 'blyat' not in message.content.lower():
        await client.send_message(message.channel, 'Блять')

    if message.content.lower() == 'kek':
        if random.choice([0, 100]):
            await client.send_message(message.channel, "Did you know that kek backwards is kek?")
        return

    if 'ayy' in message.content.lower() and 'lmao' not in message.content.lower():
        await client.send_message(message.channel, "lmao")

    if 'lmao' in message.content.lower() and 'ayy' not in message.content.lower():
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


@client.event
async def on_server_join(server):
    await client.send_message(discord.Object(id='222828628369604609'), "**__Joined {}__**".format(server.name))
    if server.id in bot.blacklist:
        client.leave_server(server)
    await create_server(server)


@client.event
async def on_ready():
    print('------')
    print(time.strftime(bot.DATE_FORMAT, time.localtime()))
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print("https://discordapp.com/oauth2/authorize?&client_id="+client.user.id + "&scope=bot&permissions=3688992")
    await client.send_message(discord.Object(id='222828628369604609'), "Bot Started")
    print('------')
    await suggest_reset()

print("Starting...\n")
client.run('token')
