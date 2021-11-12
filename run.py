import sys

from bots import UserEditsBot, ActiveUsersBot, ActiveUsersLastMonthBot


def get_bot_instance():
    arg = len(sys.argv) > 1 and sys.argv[1]
    mapping = {"edits": UserEditsBot, "active": ActiveUsersBot, "active_month": ActiveUsersLastMonthBot}
    bot_class = mapping.get(arg)
    if bot_class:
        return bot_class()


if __name__ == "__main__":
    print(get_bot_instance())
