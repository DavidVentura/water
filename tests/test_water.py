import pytest

from typing import List, Optional, Union
from water_cli.parser import execute_command, BadArguments, Flag, Repeated, MissingValues
from water_cli.utils import exclusive_flags, required_together
from water_cli.exceptions import ExclusiveFlags, MissingRequiredCombination


class Math1:
    def add(self, a: int, b: float):
        return a + b

    def add_x(self, a: int, x: int = 5):
        return a + x

    def double_if_truthy(self, a: int, double = None):
        if double:
            return 2*a
        return a

    def add_list_req(self, items: List[int]):
        return sum(items)

    def add_list(self, items: Optional[List[int]] = None):
        if not items:
            return 0
        return sum(items)

    def add_flag(self, a: int, b: float, plus_one: Flag):
        if plus_one:
            return a + b + 1
        return a + b

    def add_repeated(self, number: Repeated[float]):
        return sum(number)

    def add_repeated_factor(self, number: Repeated[float], factor: int = 1):
        return sum(number) * factor


class Str:
    def rev(self, items: List[str]):
        return items[::-1]

    def combined(self, items: List[Union[int, str]]):
        return items

    def spaces_to_dashes(self, text: str):
        return text.replace(' ', '-')

    @exclusive_flags([('reverse', 'crop_4')])
    def modify(self, value: str, reverse: Flag, crop_4: Flag):
        if reverse:
            return value[::-1]
        if crop_4:
            return value[:4]
        return value

    @required_together([('uppercase', 'word_nr')])
    def upper_word_sometimes(self, value: str, uppercase: Flag, word_nr: Optional[int] = None):
        if uppercase:
            assert word_nr is not None
            parts = value.split()
            parts[word_nr] = parts[word_nr].upper()
            return ' '.join(parts)
        return value

def test_integration_primitive():
    res = execute_command(Math1, 'add --a 10 --b 5.1')
    assert res == 15.1


def test_integration_flag_present_last():
    res = execute_command(Math1, 'add_flag --a 10 --b 5.1 --plus_one')
    assert res == 16.1


def test_integration_flag_present_first():
    res = execute_command(Math1, 'add_flag --plus_one --a 10 --b 5.1')
    assert res == 16.1


def test_integration_flag_absent():
    res = execute_command(Math1, 'add_flag --a 10 --b 5.1')
    assert res == 15.1


def test_integration_flag_repeated():
    res = execute_command(Math1, 'add_repeated --number 10 --number 5')
    assert res == 15.0


def test_integration_flag_repeated_without_repeating():
    res = execute_command(Math1, 'add_repeated --number 10')
    assert res == 10


def test_integration_flag_repeated_with_other_flag():
    res = execute_command(Math1, 'add_repeated_factor --number 10 --factor 2')
    assert res == 20


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


def test_integration_missing_list_value():
    with pytest.raises(MissingValues) as e:
        execute_command(Math1, 'add_list_req --items')
    assert str(e.value) == 'Missing values for parameters: --items'


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


def test_integration_no_args():
    with pytest.raises(BadArguments) as e:
        execute_command(Math1, '')
        assert "Received no arguments" in str(e)


def test_integration_missing_args():
    with pytest.raises(BadArguments) as e:
        execute_command(Math1, 'add --a 2')
    assert "'b'" in str(e)


def test_values_with_spaces_quoted():
    res = execute_command(Str, r'spaces_to_dashes --text "this text has spaces"')
    assert res == 'this-text-has-spaces'


def test_values_with_spaces():
    res = execute_command(Str, r'spaces_to_dashes --text this\ text\ has\ spaces')
    assert res == 'this-text-has-spaces'


def test_exclusive_flags_no_conflict():
    res = execute_command(Str, 'modify --value some_string --reverse')
    assert res == 'gnirts_emos'


def test_exclusive_flags_conflict():
    with pytest.raises(ExclusiveFlags) as e:
        execute_command(Str, 'modify --value some_string --reverse --crop_4')
    assert e.value.exclusive_flags == ('reverse' , 'crop_4')
    assert "can't be provided at the same time" in str(e.value)


def test_required_combinations_no_conflict():
    res = execute_command(Str, 'upper_word_sometimes --value "this is a sentence"')
    assert res == 'this is a sentence'
    res = execute_command(Str, 'upper_word_sometimes --value "this is a sentence" --uppercase --word_nr 3')
    assert res == 'this is a SENTENCE'


def test_required_combinations_conflict():
    with pytest.raises(MissingRequiredCombination) as e:
        execute_command(Str, 'upper_word_sometimes --value "this is a sentence" --uppercase')
