from pyswip import Prolog
import re

command_list = [
    {
        'regex': r'^Кто дружит с (.+)\?$',
        'help': 'Запрос: «Кто дружит с [Игрок]?»',
        'query': "friend('{0}',X)",
        'vars': ('X'),
        'answer': lambda players: f'C ним/ней дружит {", а еще ".join(players)}.'
    },

    {
        'regex': r'^(.+) дружит с (.+)\?$',
        'help': 'Запрос: «[Игрок А] дружит с [Игрок Б]?»',
        'query': "nickname('{0}'), nickname('{1}'),friend('{0}','{1}')",
        'vars': None,
        'answer': lambda res: "Да, это так." if res else "Нет, это не так."
    },

    {
        'regex': r'^(.+) может играть с (.+)\?$',
        'help': 'Запрос: «[Игрок А] может играть с [Игрок Б]?»',
        'query': "nickname('{0}'),nickname('{1}'),can_play_together('{0}','{1}')",
        'vars': None,
        'answer': lambda res: "Да, это так." if res else "Нет, это не так."
    },

    {
        'regex': r'^Какой ранг у (.+)\?$',
        'help': 'Запрос: «Какой ранг у [Игрок]?»',
        'query': "nickname('{0}'),player_rank('{0}',X)",
        'vars': ('X'),
        'answer': lambda level:
            'Непонятно какой ранг.' if not level
            else f'Он(а) достиг(ла) {level} ранга.'
    },
    {
        'regex': r'^С кем может играть игрок (.+)\?$',
        'help': 'Запрос: «С кем может играть игрок [Игрок]?»',
        'query': r"nickname('{0}'),can_play_with('{0}',X), X \= '{0}'",
        'vars': ('X'),
        'answer': lambda players:
            'Нет игроков с таким же рангом.' if len(players) == 0
            else f'У следующих игроков такой же ранга как и у него/нее: { ", ".join(players) }.'
    },
    {
        'regex': r'^Кто потенциальный друг (.+)\?$',
        'help': 'Запрос: «Кто потенциальный друг [Игрок]?»',
        'query': r"nickname('{0}'),potential_friends('{0}',X)",
        'vars': ('X'),
        'answer': lambda players:
            'Нет потенциальных друзей.' if len(players) == 0
            else f'Список потенциальных друзией: { ", ".join(players) }.'
    },
    {
        'regex': r'^Какие реальные имена друзей игрока (.+)\?$',
        'help': 'Запрос: «Какие реальные имена друзей игрока [Игрок]?»',
        'query': r"nickname('{0}'),friends_real_name('{0}',X)",
        'vars': ('X'),
        'answer': lambda players:
            'Нет друзей.' if len(players) == 0
            else f'Список реальных имен друзией: { ", ".join(players) }.'
    },
]
def help_messege():
    print("Используйте команду 'help', чтобы получить списко доступных запросов")
    for command in command_list:
        print(command['help'])

def init():
    try:
        prolog = Prolog()
        prolog.consult('lab-1.pl')
        return prolog
    except:
        print("Ошибка чтения базы знаний, некорректный путь!")
    return

def read_request():
    while True:
        s = input("request-for-kb>>")

        if s == "exit":
            return
        
        if s == "help":
            help_messege()
            continue
        yield s

def parse_request(req: str):
    req = re.sub(r'\s+', ' ',req.strip())

    for i in command_list:
        match = re.search(i['regex'], req, re.IGNORECASE)
        if match:
            print(match.groups())
            return i, match
    print("Проверьте корректность запроса!")
    return None

def query_in_kb(format, values, prolog: Prolog):
    result = []
    prolog = Prolog()
    prolog.consult('lab-1.pl')
    string_query = format['query'].format(*values)

    solutions = prolog.query(string_query)
    
    for sol in solutions:
        if format['vars']!=None:
            result.append(sol[format['vars']])
        else:
            result.append(sol)
    return result

def print_result(format, res):
    print(format['answer'](res))
    return


def main():
    prolog = init()
    help_messege()

    for com in read_request():
        try:
            format, match = parse_request(com)
            result = query_in_kb(format=format, values=match.groups(), prolog=prolog)
            print_result(format=format, res=result)
        except:
            continue
main()