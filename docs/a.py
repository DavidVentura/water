from typing import Optional, List
from water_cli.parser import Namespace
from water_cli.helpers import generate_docs

class c:
    class math:
        def add(self, a: int, b: int):
            """Add 2 numbers

            Examples:
              a: 5
            """
            return a + b
        def sub(self, a: int, b: int):
            return a - b
    class string:
        def join(self, items: List[str], char: Optional[str] = ' '):
            return char.join(items)

ns = Namespace.from_callable(c)
print(generate_docs(ns))
