import water_cli

class Calculator:
  """A simple calculator class."""

  def double(self, number: int):
    return 2 * number

if __name__ == '__main__':
    water_cli.simple_cli(Calculator)
