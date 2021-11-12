from datetime import datetime

import jinja2
import toolforge
from dateutil.relativedelta import relativedelta


class BaseBot:
    sql = None
    links = []
    header = None
    title = None
    frequency = None

    def __init__(self):
        self.connection = toolforge.connect("ukwiki")

    def get_header(self):
        return self.header

    def get_result(self):
        with self.connection.cursor() as cursor:
            cursor.execute(self.get_sql())
            return self.render_results(cursor.fetchall())

    @staticmethod
    def parse_results(results):
        return (
            {"user_name": user_name.decode(), "user_editcount": user_editcount}
            for user_name, user_editcount in results
        )

    def render_results(self, results):
        results = self.parse_results(results)
        with open("templates/template.jinja2") as file:
            template = jinja2.Template(file.read())
            return template.render(
                users=results,
                header=self.get_header(),
                links=self.links,
                frequency=self.frequency,
                date=datetime.today().strftime("%d.%m.%Y"),
            )

    def get_sql(self):
        return self.sql


class UserEditsBot(BaseBot):
    links = ["User:RLutsBot/Активні", "User:RLutsBot/Редагування за останній місяць"]
    header = "Список користувачів, кількість редагувань яких не менша 150"
    title = "Користувач:RLutsBot/Редагування"
    frequency = "щоденно"

    sql = """
    SELECT user_name, user_editcount FROM user 
    WHERE user_id NOT IN (SELECT ug_user FROM user_groups WHERE ug_group='bot') 
    AND user_name != 'Automatic welcomer'
    AND user_editcount >= 150 order by user_editcount desc;
    """


class ActiveUsersBot(BaseBot):
    title = "Користувач:RLutsBot/Активні"
    links = ["User:RLutsBot/Редагування", "User:RLutsBot/Редагування за останній місяць"]
    frequency = "щоденно"

    def get_header(self):
        old_date = (datetime.today() - relativedelta(months=1)).strftime("%d.%m.%Y")
        new_date = datetime.today().strftime("%d.%m.%Y")
        return f"Кількість редагувань за останній місяць ({old_date}–{new_date})"

    def get_sql(self):
        old_date = int((datetime.today() - relativedelta(months=1)).strftime("%Y%m%d000000"))
        new_date = int(datetime.today().strftime("%Y%m%d000000"))

        return f"""
        SELECT a.actor_name, COUNT(a.actor_user) CNT FROM revision AS r
        JOIN actor AS a ON (a.actor_id = r.rev_actor)
        WHERE r.rev_timestamp > {old_date} and r.rev_timestamp < {new_date}
        AND a.actor_user NOT IN (SELECT ug_user FROM user_groups WHERE ug_group='bot')
        GROUP BY a.actor_name
        ORDER BY CNT DESC
        """


if __name__ == "__main__":
    bot = ActiveUsersBot()
    print(bot.get_result())
