from water.parser import args_to_kwargs

def test_args_to_kwargs():
    res = args_to_kwargs(['--arg2', '20'])
    assert res == {'arg2': '20'}


def test_args_to_kwargs_equal():
    res = args_to_kwargs(['--arg2=20'])
    assert res == {'arg2': '20'}


def test_args_to_kwargs():
    res = args_to_kwargs(['--arg2', '20', '--arg3=5'])
    assert res == {'arg2': '20', 'arg3': '5'}
