# bot = None


class Args(list):
    async def toString(self):
        return " ".join(self)


class StartupErr(Exception):
    pass
