# Water

[![codecov](https://codecov.io/gh/davidventura/water/branch/master/graph/badge.svg?token=m5obuvwZ0I)](https://codecov.io/gh/davidventura/water)
[![Documentation Status](https://readthedocs.org/projects/water-cli/badge/?version=latest)](https://water-cli.readthedocs.io/en/latest/?badge=latest)

Water is a Python library that allows you to generate command-line interfaces (CLIs) for your Python project. Water is similar to the [Google Fire](https://github.com/google/python-fire) library, with some key differences:

- Water is type-safe. This means that Water uses type annotations to ensure that the input values are of the correct type.
- Water is designed with easy integration testing in mind. This means that you can easily test your Water CLI by invoking it from your test code, making it simple to write thorough and comprehensive tests for your CLI.

## Installation

To install Water, use `pip`:

```
pip install water-cli
```


## Getting started

Here's a simple example of how to use Water:

```python
import water_cli

def greet(name: str):
    print(f"Hello, {name}!")

if __name__ == '__main__':
    water_cli.simple_cli(greet)
```

In this example, we define a function called greet that takes a single argument, name, with type str.

When we run the script with `python script.py greet --name Alice`, Water will call the greet function with `name='Alice'`.

## Advanced usage

Please follow [the docs](https://water-cli.readthedocs.io/en/latest/?badge=latest).


## Contributing

If you find a bug or have a feature request, please open an issue on the GitHub repository. Pull requests are also welcome!

## License

Water is licensed under the MIT License.

## Testing

Python3.9, 3.11:
```
docker build -f dockerfiles/3.9-Dockerfile .
docker build -f dockerfiles/3.11-Dockerfile .
```

Development
```
poetry run pytest
```

## Releasing

```
poetry publish --build --username $PYPI_USERNAME --password $PYPI_PASSWORD
```
