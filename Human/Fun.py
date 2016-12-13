import wikipedia
import xkcd
import random
from cleverbot import Cleverbot

bot = None


async def wiki(query, sentences=3):
    if not query:
        return "Query must not be empty"
    try:
        wik = wikipedia.summary(query, sentences=sentences)
    except wikipedia.exceptions.DisambiguationError:
        wik = "Too many possible results, try: {}".format(", ".join(wikipedia.search(query)))
    except Exception as e:
        return ":x:{0}:{1}\nContact support".format(e, type(e).__name__)
    return wik


async def get_xkcd(number=0, random=False):
    if random:
        comic = xkcd.getRandomComic()
    elif number > 0 and number < (xkcd.getLatestComicNum() + 1):
        comic = xkcd.getComic(number)
    else:
        comic = xkcd.getLatestComic()

    info = []
    result = """
```xkcd #{0.number} : {0.title}```
{0.imageLink}
""".format(comic)

    info.append(result)
    info.append("***{0}***".format(comic.altText))

    return info


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


async def convo_manager(check):
    if check in bot.convos:
        return bot.convos[check]
    else:
        # *Creates a conversation for them if not
        bot.convos[check] = Cleverbot()
        return bot.convos[check]
