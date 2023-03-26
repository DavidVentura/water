# Getting Started

## Installation

You can install Water using pip:

```bash
pip install water-cli
```

## Creating Your First Command

Once Water is installed, you can use it to create a command-line interface for your Python function. Here's an example:

```python
import water_cli


@water_cli.simple_cli
def greet(name: str):
    return f"Hello, {name}!"
```
This example creates a greet command that takes a name argument and prints a greeting. You can run this command from the command line by running:

```run_example
$ python example.py greet --name World
Hello, World!
```

## Further Reading

For more information on how to use Water, check out the [Usage](./usage.md) and [Utilities](./utilities.md) sections of the documentation.
