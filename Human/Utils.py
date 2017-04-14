# bot = None


class Args(list):
    def toString(self):
        return " ".join(self)


class StartupErr(Exception):
    pass


def check_bot_server(server):
    bots = 0
    for usr in server.members:
        if usr.bot:
            bots += 1
    return round((bots / server.member_count * 100), 2)
