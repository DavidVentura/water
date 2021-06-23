# Water CLI

Library for automatically generating command-line interfaces from Python classes.

## Why Water?

The core ideas behind Water are

- The generated CLI should be fully testable
- Easy to generate docs from
- Type-inference based only on hints, not on string values

## Installation

To install with pip, run `pip install water-cli`

## Basic Usage

```python
import sys
from water_cli import execute_command

class Math1:
    def add_list(self, items: List[int]):
        if not items:
            return 0
        return sum(items)

print(execute_command(Math1, ' '.join(sys.argv)))
```

```bash
$ python example.py add_list --items 1,2,3
6
```

### Nested commands

```python
import sys
from water_cli import execute_command

class NestedObj:
    class SubCommand1:
        def double(self, number: int):
            return number * 2
        def triple(self, number: int):
            return number * 3

print(execute_command(NestedObj, ' '.join(sys.argv)))
```
```bash
$ python example.py SubCommand1 double --number 2
4
$ python example.py SubCommand1 triple --number 2
6
```


## Comparison to similar projects

### [Python Fire](https://github.com/google/python-fire)


#### Data types

`water` will cast data based on type hints instead of its value:

Assuming this command had type hints `List[str]`

|cli|input|output|
|---|-----|------|
|fire|'thing'|'thing'|
|fire|'thing,other'|['thing', 'other']|
|fire|'1'|1|
|fire|'yes'|True|
|-|-|-|
|water|'thing'|['thing']|
|water|'thing,other'|['thing', 'other']|
|water|'1'|['1']|
|water|'yes'|['yes']|

#### Testability

Calling `water_cli.parser.parse(ns, <input>)` allows you to check which arguments 
would be passed, and to which function. This allows you to test your CLI tools.
