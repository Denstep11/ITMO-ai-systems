from pyswip import Prolog
from command import Command
import re

command_list = [
    Command(
        r'^Кто дружит с (.+)\?$',
        'Запрос: «Кто дружит с [Игрок]?»',
        "friend('{0}',X)",
        ('X'),
        lambda players: 'Игкрок дружит с '+", ".join(players) + '.'
    ),
    Command(
        r'^(.+) дружит с (.+)\?$',
        'Запрос: «[Игрок А] дружит с [Игрок Б]?»',
        "friend('{0}','{1}')",
        None,
        lambda res: "Да!" if res else "Нет:("
    ),
    Command(
        r'^(.+) может играть с (.+)\?$',
        'Запрос: «[Игрок А] может играть с [Игрок Б]?»',
        "can_play_together('{0}','{1}')",
        None,
        lambda res: "Да!" if res else "Нет:("
    ),
    Command(
        r'^Какой ранг у (.+)\?$',
        'Запрос: «Какой ранг у [Игрок]?»',
        "player_rank('{0}',X)",
        ('X'),
        lambda rank: 'Непонятно какой ранг.' if not rank else 'Игрок достиг ранг ' + "".join(rank) + '.'
    ),
    Command(
        r'^С кем может играть игрок (.+)\?$',
        'Запрос: «С кем может играть игрок [Игрок]?»',
        "can_play_with('{0}',X), X \= '{0}'",
        ('X'),
        lambda players:
            'Нет игроков с таким же рангом, игроку не с кем играть(' if not players
            else 'Игрок может играсть с этими игроками: ' + ", ".join(players) + '.'
    ),
    Command(
        r'^Кто потенциальный друг (.+)\?$',
        'Запрос: «Кто потенциальный друг [Игрок]?»',
        r"potential_friends('{0}',X)",
        ('X'),
        lambda players:
            'Нет потенциальных друзей.' if not players
            else 'Список потенциальных друзией: ' + ", ".join(players) + '.'
    ),
    Command(
        r'^Какие реальные имена друзей игрока (.+)\?$',
        'Запрос: «Какие реальные имена друзей игрока [Игрок]?»',
        r"friends_real_name('{0}',X)",
        ('X'),
        lambda players:
            'Нет друзей.' if len(players) == 0
            else f'Список реальных имен друзией: ' + ", ".join(players) + '.'
    ),
]

def help_messege():
    print("Используйте команду 'help', чтобы получить списко доступных запросов")
    for command in command_list:
        print(command.help)

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
        match = re.search(i.regex, req, re.IGNORECASE)
        if match:
            return i, match

    print("Проверьте корректность запроса!")
    return None

def query_in_kb(command, values, prolog: Prolog):
    result = []
    prolog = Prolog()
    prolog.consult('lab-1.pl')
    string_query = command.query.format(*values)

    solutions = prolog.query(string_query)
    
    for sol in solutions:
        if command.vars != None:
            result.append(sol[command.vars])
        else:
            result.append(sol)

    return result

def print_result(command, res):
    print(command.answer(res))
    return


def main():
    prolog = init()
    help_messege()

    for com in read_request():
        try:
            command, match = parse_request(com)
            result = query_in_kb(command=command, values=match.groups(), prolog=prolog)
            print_result(command=command, res=result)
        except:
            print("Возникла ошибка!")
            continue
main()