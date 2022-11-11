from typing import List

class BadArguments(ValueError):
    pass

class BadSubcommand(BadArguments):
    def __init__(self, parent: List[str], attempted: str, valid_options: List[str]):
        self.parent = parent
        self.attempted = attempted
        self.valid_options = valid_options

    def __str__(self) -> str:
        if len(self.parent) > 1:
            return f"'{' '.join(self.parent[1:])}' has no sub-command '{self.attempted}'."
        return f"No top-level command '{self.attempted}'."

class MissingParameters(BadArguments):
    def __init__(self, params: List[str]):
        self.params = params
    def __str__(self) -> str:
        _params = [f'--{p}' for p in self.params]
        return f"Missing parameters: {', '.join(_params)}"

class UnexpectedValue(BadArguments):
    def __init__(self, value: str):
        self.value = value
    def __str__(self) -> str:
        return f"Expected a parameter (--parameter) but got a value: {self.value}. Did you mean --{self.value}?"

class UnexpectedParameters(BadArguments):
    def __init__(self, params: List[str]):
        self.params = params
    def __str__(self) -> str:
        _params = [f'--{p}' for p in self.params]
        return f"Unexpected parameters: {', '.join(_params)}"

class ConsecutiveValues(BadArguments):
    def __init__(self, last_key: str, last_value: str, arg: str):
        self.last_key = last_key
        self.last_value = last_value
        self.attempted = arg

    def __str__(self) -> str:
        return (f'Attempted to pass multiple values to option (--{self.last_key} {self.last_value} {self.attempted}). '
                f'Did you mean --{self.attempted}?')
