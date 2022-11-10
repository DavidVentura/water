import pytest

from water_cli.parser import execute_command, args_to_kwargs
from water_cli.exceptions import BadArguments, BadSubcommand, ConsecutiveValues, MissingParameters, UnexpectedParameters, UnexpectedValue

class Math1:
    class Math2:
        def sub(self, a: int, b: float):
            return a - b
    def add(self, a: int, b: float):
        return a + b
    def add2(self, a: int, b: float, c: int):
        return a + b


def test_args_to_kwargs_double_value():
    with pytest.raises(BadArguments) as e:
        args_to_kwargs(['--arg2', '20', 'this is double'])
    assert 'double' in str(e)


def test_no_subcommand_toplevel():
    with pytest.raises(BadSubcommand) as e:
        execute_command(Math1, 'this_does_not_exist --a 10 --b 5.1')
    assert e.value.parent == ['Math1']
    assert e.value.attempted == 'this_does_not_exist'
    assert str(e.value) == "'Math1' has no sub-command 'this_does_not_exist'"


def test_no_subcommand_nested():
    with pytest.raises(BadSubcommand) as e:
        execute_command(Math1, 'Math2 this_does_not_exist --a 10 --b 5.1')
    assert e.value.parent == ['Math1', 'Math2']
    assert e.value.attempted == 'this_does_not_exist'


def test_value_without_flag():
    with pytest.raises(UnexpectedValue) as e:
        execute_command(Math1, 'add 5')
    assert e.value.value == '5'
    assert str(e.value) == 'Expected a parameter (--parameter) but got a value: 5. Did you mean --5?'


def test_double_value():
    with pytest.raises(ConsecutiveValues) as e:
        execute_command(Math1, 'add --a 10 b 20')
    assert e.value.last_key == 'a'
    assert e.value.last_value == '10'
    assert e.value.attempted == 'b'
    assert '--a 10 b' in str(e.value)
    assert 'mean --b?' in str(e.value)


def test_missing_parameters():
    with pytest.raises(MissingParameters) as e:
        execute_command(Math1, 'add --a 10')
    assert e.value.params == ['b']
    assert str(e.value) == 'Missing parameters: --b'


def test_missing_parameters_multiple():
    with pytest.raises(MissingParameters) as e:
        execute_command(Math1, 'add2 --a 10')
    assert e.value.params == ['b', 'c']
    assert str(e.value) == 'Missing parameters: --b, --c'


def test_unexpected_parameters():
    with pytest.raises(UnexpectedParameters) as e:
        execute_command(Math1, 'add --a 10 --b 20 --c 30')
    assert e.value.params == ['c']
    assert str(e.value) == 'Unexpected parameters: --c'


def test_unexpected_parameters_multiple():
    with pytest.raises(UnexpectedParameters) as e:
        execute_command(Math1, 'add --a 10 --b 20 --c 30 --d 40')
    assert e.value.params == ['c', 'd']
    assert str(e.value) == 'Unexpected parameters: --c, --d'
