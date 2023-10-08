class Command():
    def __init__(self, regex, help, query, vars, answer) -> None:
        self.regex = regex
        self.help = help
        self.query = query
        self.vars = vars
        self.answer = answer