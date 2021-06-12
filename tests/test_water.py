import pytest

from typing import List, Optional, Union
from water_cli.parser import execute_command, BadArguments


class Math1:
    def add(self, a: int, b: float):
        return a + b

    def add_x(self, a: int, x: int = 5):
        return a + x

    def double_if_truthy(self, a: int, double = None):
        if double:
            return 2*a
        return a

    def add_list(self, items: Optional[List[int]] = None):
        if not items:
            return 0
        return sum(items)


class Str:
    def rev(self, items: List[str]):
        return items[::-1]

    def combined(self, items: List[Union[int, str]]):
        return items


def test_integration_primitive():
    res = execute_command(Math1, 'add --a 10 --b 5.1')
    assert res == 15.1


def test_integration_typed():
    res = execute_command(Str, 'rev --items a,b,c,d')
    assert res == ['d', 'c', 'b', 'a']


def test_integration_default():
    res = execute_command(Math1, 'add_x --a 1')
    assert res == 6


def test_integration_override_default():
    res = execute_command(Math1, 'add_x --a 1 --x=1')
    assert res == 2


def test_integration_default_falsy():
    res = execute_command(Math1, 'double_if_truthy --a 1')
    assert res == 1


def test_integration_override_default_truthy():
    res = execute_command(Math1, 'double_if_truthy --a 1')
    assert res == 1


def test_integration_override_default_compound_type_1():
    res = execute_command(Math1, 'add_list --items 1')
    assert res == 1


def test_integration_override_default_compound_type_2():
    res = execute_command(Math1, 'add_list --items 1,2,3')
    assert res == 6


def test_integration_compound_type():
    res = execute_command(Str, 'combined --items b,2')
    assert res == ['b', 2]


def test_integration_extra_args():
    with pytest.raises(BadArguments) as e:
        execute_command(Math1, 'add --a 2 --b 3 --c 4')
    assert "'c'" in str(e)


def test_integration_missing_args():
    with pytest.raises(BadArguments) as e:
        execute_command(Math1, 'add --a 2')
    assert "'b'" in str(e)
