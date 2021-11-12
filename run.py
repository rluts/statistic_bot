import sys

import pywikibot

from bots import UserEditsBot, ActiveUsersBot, ActiveUsersLastMonthBot


class BotRunner:
    mapping = {"edits": UserEditsBot, "active": ActiveUsersBot, "active_month": ActiveUsersLastMonthBot}

    def __init__(self):
        self.site = pywikibot.Site("uk", "wikipedia")

    def get_bot_instance(self):
        arg = len(sys.argv) > 1 and sys.argv[1]
        bot_class = self.mapping.get(arg)
        if bot_class:
            return bot_class()

    def get_page(self, page_name):
        return pywikibot.Page(self.site, page_name)

    def run(self):
        bot_instance = self.get_bot_instance()
        if not bot_instance:
            raise ValueError(f"Please use one of the parameter: {', '.join(self.mapping.keys())}")
        page = self.get_page(bot_instance.title)
        wiki_text = bot_instance.get_result()
        page.text = wiki_text
        page.save()


if __name__ == "__main__":
    BotRunner().run()
