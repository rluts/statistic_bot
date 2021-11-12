from datetime import datetime

import jinja2
import toolforge


class BaseBot:
    sql = None
    links = []
    header = None
    title = None
    frequency = None

    def __init__(self):
        self.connection = toolforge.connect("ukwiki")

    def get_result(self):
        with self.connection.cursor() as cursor:
            cursor.execute(self.get_sql())
            return self.render_results(cursor.fetchall())

    def parse_results(self, results):
        raise NotImplemented

    def render_results(self, results):
        results = self.parse_parameters(results)
        with open("templates/template.jinja2") as file:
            template = jinja2.Template(file.read())
            return template.render(
                users=results,
                header=self.header,
                links=self.links,
                frequency=self.frequency,
                date=datetime.today().strftime("%d-%m-%Y"),
            )

    def get_sql(self):
        return self.sql


class RecentPagesBot(BaseBot):
    sql = """
    SELECT user_name, user_editcount FROM user 
    WHERE user_id NOT IN (SELECT ug_user FROM user_groups WHERE ug_group='bot') 
    AND user_editcount >= 150 order by user_editcount desc;
    """
    links = ["User:RLutsBot/Активні", "User:RLutsBot/Редагування"]
    header = "Список користувачів, кількість редагувань яких не менша 150"
    title = "Користувач:RLutsBot/Редагування"
    frequency = "щоденно"

    def parse_results(self, results):
        return (
            {"user_name": user_name.decode(), "user_editcount": user_editcount}
            for user_name, user_editcount in results
        )


if __name__ == "__main__":
    bot = RecentPagesBot()
    print(bot.get_result())
