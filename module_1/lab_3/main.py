from pyswip import Prolog
import re

command_list = [
    {
        'regex': r'^Кто дружит с (.+)\?$',
        'help': 'Запрос: «Кто дружит с [Игрок]?»',
        'query': "friend('{0}',X)",
        'vars': ('X'),
        'answer': lambda players: 'Игкрок дружит с '+", ".join(players) + '.'
    },

    {
        'regex': r'^(.+) дружит с (.+)\?$',
        'help': 'Запрос: «[Игрок А] дружит с [Игрок Б]?»',
        'query': "friend('{0}','{1}')",
        'vars': None,
        'answer': lambda res: "Да!" if res else "Нет:("
    },

    {
        'regex': r'^(.+) может играть с (.+)\?$',
        'help': 'Запрос: «[Игрок А] может играть с [Игрок Б]?»',
        'query': "can_play_together('{0}','{1}')",
        'vars': None,
        'answer': lambda res: "Да!" if res else "Нет:("
    },

    {
        'regex': r'^Какой ранг у (.+)\?$',
        'help': 'Запрос: «Какой ранг у [Игрок]?»',
        'query': "player_rank('{0}',X)",
        'vars': ('X'),
        'answer': lambda rank: 'Непонятно какой ранг.' if not rank else 'Игрок достиг ' + "".join(rank) + ' ранга.'
    },
    {
        'regex': r'^С кем может играть игрок (.+)\?$',
        'help': 'Запрос: «С кем может играть игрок [Игрок]?»',
        'query': r"can_play_with('{0}',X), X \= '{0}'",
        'vars': ('X'),
        'answer': lambda players:
            'Нет игроков с таким же рангом, игроку не с кем играть(' if not players
            else 'Игрок может играсть с этими игроками: ' + ", ".join(players) + '.'
    },
    {
        'regex': r'^Кто потенциальный друг (.+)\?$',
        'help': 'Запрос: «Кто потенциальный друг [Игрок]?»',
        'query': r"potential_friends('{0}',X)",
        'vars': ('X'),
        'answer': lambda players:
            'Нет потенциальных друзей.' if not players
            else 'Список потенциальных друзией: ' + ", ".join(players) + '.'
    },
    {
        'regex': r'^Какие реальные имена друзей игрока (.+)\?$',
        'help': 'Запрос: «Какие реальные имена друзей игрока [Игрок]?»',
        'query': r"friends_real_name('{0}',X)",
        'vars': ('X'),
        'answer': lambda players:
            'Нет друзей.' if len(players) == 0
            else f'Список реальных имен друзией: ' + ", ".join(players) + '.'
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

        if s == "":
            continue

        yield s

def parse_request(req: str):
    req = re.sub(r'\s+', ' ',req.strip())

    for i in command_list:
        match = re.search(i['regex'], req, re.IGNORECASE)
        if match:
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
            print("возникла ошибка")
            continue
main()