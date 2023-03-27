# Usage

## Simple function

Here's an example of how to use Water to generate a CLI for a Python function:

```python
import water_cli


def add(x: int, y: int):
    return x + y


if __name__ == "__main__":
    water_cli.simple_cli(add)
```

In this example, we define the `add` function to take two integer arguments, `x` and `y`, and print their sum. Finally, we call `water_cli.simple_cli(add)` to generate a CLI for the `add` function.

When we run this script from the command line, we can use the `add` command with the `--x` and `--y` flags to pass values for `x` and `y`, respectively:

```run_example
$ python example.py add --x 1 --y 2
3
```

## Grouped commands

Water also supports the ability to group related commands under a single command group. Here's an example of how to use command groups:

```python
import water_cli


class Group:
    class math:
        def add(self, x: int, y: int):
            return x + y

        def subtract(self, x: int, y: int):
            return x - y


if __name__ == "__main__":
    water_cli.simple_cli(Group)
```

In this example, we define a command group called `math` by creating a class. Inside the `math` class, we define two commands: `add` and `subtract`.

When we run this script from the command line, we can use the `math` command to access the `add` and `subtract` sub-commands:

```run_example
$ python example.py math add --x 1 --y 2
3
$ python example.py math subtract --x 5 --y 2
3
```

## Required vs Optional parameters

When defining command-line interfaces, it's often useful to distinguish between required and optional parameters.

### Required Parameters

To define a required parameter, you can simply omit the default value of the parameter in the function signature. For example:
```python
from water_cli import simple_cli


@simple_cli
def greet(name: str):
    return f"Hello, {name}!"
```

In this example, the `name` parameter is required since there is no default value specified. If you try to call the `greet` function without passing a value for `name`, you'll get a `MissingParameters` exception.

```run_example
$ python example.py greet --name World
Hello, World!
$ python example.py greet
Missing parameters: --name
```


### Optional Parameters

To define an optional parameter, you can specify a default value for the parameter in the function signature. For example:
```python
from water_cli import simple_cli


@simple_cli
def greet(name: str = "World"):
    return f"Hello, {name}!"
```

In this example, the `name` parameter is optional since it has a default value of `"World"`. If you call the `greet` function without passing a value for `name`, it will use the default value instead.
```run_example
$ python example.py greet
Hello, World!
$ python example.py greet --name Alice
Hello, Alice!
```
### Mixing Required and Optional Parameters

You can mix required and optional parameters in the same function signature. Required parameters should be listed before optional parameters. For example:
```python
from water_cli import simple_cli


@simple_cli
def greet(name: str, times: int = 1):
    ret = []
    for i in range(times):
        ret.append(f"Hello, {name}!")
    return "\n".join(ret)
```

In this example, `name` is a required parameter since it has no default value, while `times` is an optional parameter with a default value of `1`. If you call the `greet` function with only a value for `name`, it will use the default value for `times`. If you call it with both `name` and `times`, it will use the values you provided.

```run_example
$ python example.py greet --name Alice
Hello, Alice!
$ python example.py greet --name Alice --times 2
Hello, Alice!
Hello, Alice!
```

## Utility types

### Repeated

`water` supports the `Repeated` type annotation, which allows an option to be repeated on the command line. Here's an example:

```python
import water_cli


def my_function(fruit: water_cli.Repeated[str]):
    return f"The fruits are {', '.join(fruit)}."


if __name__ == "__main__":
    water_cli.simple_cli(my_function)
```

```run_example
$ python example.py my_function --fruit apple --fruit banana
The fruits are apple, banana.
```

In this example, `fruit` is declared as a `water_cli.Repeated[str]`, which means it's a string that can be repeated multiple times. When we pass `--fruit apple --fruit banana` as command line arguments, `water` automatically converts the repeated `--fruit` options into a list of strings, which is passed to the `my_function` implementation. This means that inside the `my_function` implementation, `fruit` is a Python list of strings, and we can use list operations on it directly.

### Flag

`water` also supports the `Flag` type annotation, which allows an option to be specified on the command line without a value. Here's an example:

```python
import water_cli


def greet(name: str, formal_greeting: water_cli.Flag):
    if formal_greeting:
        return f"Good day, {name}!"
    else:
        return f"Hello, {name}!"


if __name__ == "__main__":
    water_cli.simple_cli(greet)
```

```run_example
$ python example.py greet --name Alice --formal-greeting
Good day, Alice!
$ python example.py greet --name Alice
Hello, Alice!
```

In this example, `formal_greeting` is declared as a `water_cli.Flag`, which means it's a boolean option that can be either present or absent on the command line. When we pass `--name Alice --formal-greeting` as command line arguments, `water` automatically sets `formal_greeting` to `True` because it appears on the command line. If we omit `--formal-greeting`, `water` sets `formal_greeting` to `False`.
