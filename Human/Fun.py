import wikipedia

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
