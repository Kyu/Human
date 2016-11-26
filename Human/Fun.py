import wikipedia
import xkcd


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
