import jinja2
import toolforge


class BaseBot:
    sql = None
    links = []
    header = None
    title = None
    frequency = None

    def __init__(self):
        self.connection = toolforge.connect('ukwiki')

    def get_result(self):
        with self.connection.cursor() as cursor:
            cursor.execute(self.get_sql())
            return self.render_results(cursor.fetchall())

    @staticmethod
    def render_results(results):
        results = ({'user_name': user_name, user_editcount: user_editcount} for user_name, user_editcount in results)
        with open('templates/template.jinja2') as file:
            template = jinja2.Template(file.read())
            return template.render(users=results)

    def get_sql(self):
        return self.sql


class RecentPagesBot(BaseBot):
    sql = """
    SELECT user_name, user_editcount FROM user 
    WHERE user_id NOT IN (SELECT ug_user FROM user_groups WHERE ug_group='bot') 
    AND user_editcount >= 150 order by user_editcount desc;
    """
    links = ["User:RLutsBot/Активні", "User:RLutsBot/Редагування"]
    header = "Список користувачів, кількість редагувань яких не менша 100"
    title = "Користувач:RLutsBot/Редагування"
    frequency = "щоденно"


if __name__ == '__main__':
    bot = RecentPagesBot()
    print(bot.get_result())