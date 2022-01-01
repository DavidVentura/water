import pytest

from water_cli.parser import args_to_kwargs, BadArguments


def test_args_to_kwargs_double_value():
    with pytest.raises(BadArguments) as e:
        args_to_kwargs(['--arg2', '20', 'this is double'])
    assert 'double' in str(e)
