# Usage

## Simple function

Here's an example of how to use Water to generate a CLI for a Python function:

```python
import water_cli

def add(x: int, y: int):
    return x + y

if __name__ == '__main__':
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

if __name__ == '__main__':
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
    return '\n'.join(ret)
```

In this example, `name` is a required parameter since it has no default value, while `times` is an optional parameter with a default value of `1`. If you call the `greet` function with only a value for `name`, it will use the default value for `times`. If you call it with both `name` and `times`, it will use the values you provided.

```run_example
$ python example.py greet --name Alice
Hello, Alice!
$ python example.py greet --name Alice --times 2
Hello, Alice!
Hello, Alice!
```

## Type-based behavior

### Enum

```python
import enum
import water_cli

class Fruit(enum.Enum):
    apple = enum.auto()
    banana = enum.auto()
    orange = enum.auto()

def eat_fruit(fruit: Fruit):
    return f"Eating {fruit.name}... yum!"

if __name__ == '__main__':
    water_cli.simple_cli(eat_fruit)
```

In this example, we define an enum called `Fruit` with three members: `apple`, `banana`, and `orange`. Each member is associated with an opaque value.

We then define a function called `eat_fruit` that takes a single argument, `fruit`, with type `Fruit`. When this function is called from the command line, Water will generate a CLI interface that allows the user to choose one of the three available fruits.

For example, if the above code is saved in a file called `example.py`, we can run the following command:

```run_example
$ python example.py eat_fruit --fruit apple
Eating apple... yum!
```

This will call the `eat_fruit` function and pass in the argument `fruit=Fruit.APPLE`. Water will validate that the `fruit` argument is one of the valid enum members, and will raise an error if an invalid value is used:

```run_example
$ python example.py eat_fruit --fruit potato
Unable to convert 'potato' to type 'Fruit': 'potato'
```

### List


```python
import water_cli
from typing import List

def my_function(name: str, numbers: List[int]):
    print(f"Hello, {name}!")
    return f"The sum of the numbers is: {sum(numbers)}"

if __name__ == '__main__':
    water_cli.simple_cli(my_function)
```

In this example, we define a `my_function` command that takes two arguments: `name`, which is a string, and `numbers` which is a list of integers. When we run the `my_function` command, we pass the `numbers` argument as a comma-separated string:

```run_example
$ python example.py my_function --name Alice --numbers 1,2,3,4,5
Hello, Alice!
The sum of the numbers is: 15
```

When we pass `--numbers 1,2,3,4,5` as a command-line argument, `water` automatically converts the input to a list of integers. This means that inside the `my_function` implementation, `numbers` is a Python list of integers, and we can perform arithmetic operations on it directly without the need for type conversions.

### Repeated

`water` supports the `Repeated` type annotation, which allows an option to be repeated on the command line. Here's an example:

```python
import water_cli

def my_function(fruit: water_cli.Repeated[str]):
    return f"The fruits are {', '.join(fruit)}."

if __name__ == '__main__':
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

if __name__ == '__main__':
    water_cli.simple_cli(greet)
```

```run_example
$ python example.py greet --name Alice --formal-greeting
Good day, Alice!
$ python example.py greet --name Alice
Hello, Alice!
```

In this example, `formal_greeting` is declared as a `water_cli.Flag`, which means it's a boolean option that can be either present or absent on the command line. When we pass `--name Alice --formal-greeting` as command line arguments, `water` automatically sets `formal_greeting` to `True` because it appears on the command line. If we omit `--formal-greeting`, `water` sets `formal_greeting` to `False`.
