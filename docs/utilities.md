# Utils

The "Utils" section of the water library provides decorators and functions that help you make the most out of your command-line interfaces.

### `exclusive_flags`

The `exclusive_flags` decorator is used to specify that a set of flags are mutually exclusive. The decorator takes a list of tuples, where each tuple represents the sets of flags that are mutually exclusive.

```python
from water_cli import exclusive_flags, simple_cli


@simple_cli
@exclusive_flags([("a", "b"), ("c", "d", "e")])
def my_func(a=False, b=False, c=False, d=False, e=False):
    pass
```

In this example, if the user passes `--a`, they cannot pass `--b`, and vice versa. Similarly, if the user passes `--c`, they cannot pass `--d` or `--e`, and vice versa.

```run_example
$ python my_script.py my_func --a some_value
$ python my_script.py my_func --a some_value --b should_fail
The flags: --a, --b can't be provided at the same time
```

### `required_together`

The `required_together` decorator is used to specify that a set of flags must be passed together. The decorator takes a list of tuples, where each tuple represents the sets of flags that must be passed together.
```python
from water_cli import required_together, simple_cli


@required_together([("a", "b"), ("c", "d")])
def my_func(a=None, b=None, c=None, d=None):
    pass


if __name__ == "__main__":
    simple_cli(my_func)
```

In this example, if the user passes `--a` they must pass `--b`, and if they pass `--c` they must also pass `--d`.

```run_example
$ python my_script.py my_func --a some_value --c other_value
Passing the flags --a also requires the flags: --b to be provided
```

# Combining `required_together` and `exclusive_flags`

These two decorators can be used at once, for convenient handling of some common operations.

```python
from water_cli import required_together, exclusive_flags, simple_cli


@required_together([("username", "password"), ("api_key", "api_token")])
@exclusive_flags([("username", "api_key")])
def login(username=None, password=None, api_key=None, api_token=None):
    pass


if __name__ == "__main__":
    simple_cli(login)
```

```run_example
$ python my_script.py login --username some_value --api_token other_value
Passing the flags --username also requires the flags: --password to be provided
$ python my_script.py login --username some_value --password my_password --api_key my_key --api_token some_token
The flags: --username, --api_key can't be provided at the same time
```


### `simple_cli`

The `simple_cli` function is used to create a CLI for a function. The function takes a function as input and generates a CLI based on the function's signature.

```python
from water_cli import simple_cli


def my_func(name: str, age: int):
    return f"{name} is {age} years old."


if __name__ == "__main__":
    simple_cli(my_func)
```

This code will generate a CLI that accepts `name` and `age` as arguments:bash
```run_example
$ python my_script.py my_func --name Alice --age 30
Alice is 30 years old.
```

When `simple_cli` is called, it parses the function's signature and generates a CLI that maps the command-line arguments to the function's parameters.
