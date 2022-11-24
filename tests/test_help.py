from water_cli.parser import Namespace
from water_cli.help_flag import add_help_flag

class FlatObj:
    @add_help_flag
    def fn1(self, number: int) -> None:
        """
        This is the doc for fn1.
        """
        pass

    @add_help_flag
    def fn2(self, *, number: int):
        """
        This is the doc for fn1.
        """
        pass

    @add_help_flag
    def fn3(self, arg1: int, arg2: int):
        """
        This is the doc for fn1.
        """
        pass

    @add_help_flag
    def fn4(self, arg1: int, arg2=5):
        """
        This is the doc for fn1.
        """
        pass

    @add_help_flag
    def no_args(self):
        """
        This is the doc for fn1.
        """
        pass


def test_namespace():
    res = Namespace.from_callable(FlatObj)
    assert res.name == 'FlatObj'
    assert res.members == []
    assert len(res.callables) == 5
    assert [c.name for c in res.callables] == ['fn1', 'fn2', 'fn3', 'fn4', 'no_args']
    assert len(res.callables[0].args) == 2
    assert res.callables[0].args[0].name == 'number'
    assert res.callables[0].args[1].name == 'help'

    assert len(res.callables[3].args) == 3
    assert res.callables[3].args[0].name == 'arg1'
    assert res.callables[3].args[1].name == 'arg2'
    assert res.callables[3].args[2].name == 'help'
    assert res.callables[3].args[1].default == 5
