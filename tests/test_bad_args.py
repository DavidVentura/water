import pytest

from water_cli.parser import args_to_kwargs, BadArguments


def test_args_to_kwargs_dangling():
    with pytest.raises(BadArguments) as e:
        args_to_kwargs(['--arg2', '20', '--arg3'])
    assert 'arg3' in str(e)

