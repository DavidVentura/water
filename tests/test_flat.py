from water_cli.parser import Namespace

class FlatObj:
    def fn1(self, number: int):
        pass

    def fn2(self, *, number: int):
        pass

    def fn3(self, arg1: int, arg2: int):
        pass

    def fn4(self, arg1: int, arg2=5):
        pass

    def no_args(self):
        pass


def test_namespace():
    res = Namespace.from_callable(FlatObj)
    assert res.name == 'FlatObj'
    assert res.members == []
    assert len(res.callables) == 5
    assert [c.name for c in res.callables] == ['fn1', 'fn2', 'fn3', 'fn4', 'no_args']
    assert len(res.callables[0].args) == 1
    assert res.callables[0].args[0].name == 'number'

    assert len(res.callables[3].args) == 2
    assert res.callables[3].args[0].name == 'arg1'
    assert res.callables[3].args[1].name == 'arg2'
    assert res.callables[3].args[1].default == 5
