# Water

Like [fire](https://github.com/google/python-fire)

This python library parses classes so that they can be executed as commands.  
In contrast with fire, there is no "automatic" type casting -- the type casting is 100% based on type hints.

# Examples

## Type casting

```python
class Math1:
    def add_list(self, items: Optional[List[int]] = None):
        if not items:
            return 0
        return sum(items)

# `items` casted to a list of `int`
res = execute_command(Math1, 'add_list --items 1,2,3')
assert res == 6

# `items` casted to a list of `int`, even though there is only one entry
res = execute_command(Math1, 'add_list --items 1')
assert res == 1
```

## Nested commands

```python
class NestedObj:
    class Inside1:
        def fn1(self, number: int):
            return number

res = execute_command(NestedObj, 'Inside1 fn1 --number 1')
assert res == 1
```
