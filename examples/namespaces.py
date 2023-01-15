import water_cli

class Tools:
    class Calculator:
      """A simple calculator class."""

      def double(self, number: int):
        return 2 * number

    class String:
        """A simple string utility class."""
        def reverse(self, string: str):
            return string[::-1]

if __name__ == '__main__':
    water_cli.simple_cli(Tools)

