from water_cli.parser import args_to_kwargs


def test_args_to_kwargs():
    res = args_to_kwargs(['--arg2', '20'])
    assert res == {'arg2': '20'}


def test_args_to_kwargs_equal():
    res = args_to_kwargs(['--arg2=20'])
    assert res == {'arg2': '20'}


def test_args_to_kwargs2():
    res = args_to_kwargs(['--arg2', '20', '--arg3=5'])
    assert res == {'arg2': '20', 'arg3': '5'}


def test_args_with_flag():
    res = args_to_kwargs(['--arg2', '20', '--activate'])
    assert res == {'arg2': '20', 'activate': None}


def test_args_with_dash_become_underscore():
    res = args_to_kwargs(['--with-dashes', '1'])
    assert res == {'with_dashes': '1'}
