# Water

[![codecov](https://codecov.io/gh/davidventura/water/branch/master/graph/badge.svg?token=m5obuvwZ0I)](https://codecov.io/gh/davidventura/water)

Like [fire](https://github.com/google/python-fire)

This python library parses classes so that they can be executed as commands.  
In contrast with fire, there is no "automatic" type casting -- the type casting is 100% based on type hints.

## Type casting

When calling `execute_command` the values passed in the command get casted to the annotated types on the function
signature.

Supported types:

* int, float
* bool: the strings `['true', '1', 't', 'y']` are considered true.
* lists, tuples: input is split by comma (`,`) and each element is casted independently.
* enum
* Union[]: gets casted to all options in order, first success is returned.
  * `Optional[type]` is `Union[type, NoneType]`
* `water.Flag`: flag, only denotes the switch was present.
* `water.Repeated[T]`: Effectively the same as `List[T]` but allows flags to be repeated and values will be concatenated

## Utilities

* `exclusive_flags` forbids certain flag combinations to be used at the same time.
  * If `--a` and `--b` are exclusive, executing `command --a --b` causes an error.
* `required_together` requires certain flag combinations to be used at the same time.
  * If `--a` and `--b` are required together, executing `command --a` or `command --b` causes an error.

# Examples

An example on a simple class

```python
import water_cli

class Calculator:
  """A simple calculator class."""

  def double(self, number: int):
    return 2 * number

if __name__ == '__main__':
    water_cli.simple_cli(Calculator)
```

```bash
$ python3 examples/calculator.py double --number 10
20
$ python3 examples/calculator.py double --number banana
Unable to convert 'banana' to type 'int': invalid literal for int() with base 10: 'banana'
```

An example on a nested class

```python
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
```

```bash
$ python3 examples/namespaces.py String reverse --string "some long string"
gnirts gnol emos
$ python3 examples/namespaces.py Calculator double --number 10
20
```
# Testing

Python3.9, 3.11:
```
docker build -f dockerfiles/3.9-Dockerfile .
docker build -f dockerfiles/3.11-Dockerfile .
```

Development
```
poetry run pytest
```

# Releasing

```
poetry publish --build --username $PYPI_USERNAME --password $PYPI_PASSWORD
```
