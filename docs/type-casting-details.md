# Type Casting details

The `water` library provides type casting functionality for command-line arguments, allowing users to easily specify the expected types for their parameters.

`water-cli` automatically handles type casting for function arguments based on the provided type information. The library supports built-in Python types, as well as custom types with proper type annotations.


### Built-in Types

`water-cli` supports the following built-in Python types:
* `str`
* `int`
* `float`
* `bool`
* `list`
* `tuple`
* `dict`

When you provide the type annotation for a function argument, `water-cli` will automatically parse and cast the input from the command line to the appropriate type. For example:
```python
import water_cli

@water_cli.simple_cli
def calculate_area(length: float, width: float) -> float:
    return length * width
```

In this case, the library will ensure that `length` and `width` are converted to `float` before calling the `calculate_area` function.

## Generic Containers
`water-cli` also supports type casting for generic types such as `List` and `Tuple`. When using these types, you can specify the type of the elements inside the container.

### List

To cast an input to a list with elements of a specific type, use the `typing.List` generic. For example, if you want to accept a list of integers as input:

```python
import water_cli
from typing import List


@water_cli.simple_cli
def sum_numbers(numbers: List[int]) -> int:
    return sum(numbers)
```

When providing input to this function via the command line, you can use a comma-separated string of integers, and `water-cli` will automatically cast the input to a list with `int` elements:

```run_example
$ python your_script.py sum_numbers --numbers 1,2,3,4,5
15
```

This will call the `sum_numbers` function with `numbers` as `[1, 2, 3, 4, 5]`.

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


if __name__ == "__main__":
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
Unable to convert 'potato' to type 'Fruit': Valid choices are: ['apple', 'banana', 'orange']
```


### Tuple and other Generics

Similarly, you can use `typing.Tuple` and other generic types to specify the types of elements within the container. For example:

```python
import water_cli
from typing import Tuple


@water_cli.simple_cli
def display_coordinates(coords: Tuple[float, float]) -> str:
    return f"Coordinates ({coords[0]}, {coords[1]})"
```

When providing input to this function via the command line, you can use a comma-separated string of floats, and `water-cli` will automatically cast the input to a tuple with `float` elements:

```run_example
$ python your_script.py display_coordinates --coords 12.5,45.3
Coordinates (12.5, 45.3)
```

This will call the `display_coordinates` function with `coords` as `(12.5, 45.3)`.

Keep in mind that for other generic types, the input format and casting will work similarly, as long as you provide the correct type annotations.
