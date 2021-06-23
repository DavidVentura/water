from water_cli.parser import Namespace

class FlatObj:
    def fn1(self, number):
        pass

    def fn2(self, *, number):
        pass

    def fn3(self, arg1, arg2):
        pass

    def fn4(self, arg1, arg2=5):
        pass


def test_namespace():
    res = Namespace.from_callable(FlatObj)
    assert res.name == 'FlatObj'
    assert res.members == []
    assert len(res.callables) == 4
    assert [c.name for c in res.callables] == ['fn1', 'fn2', 'fn3', 'fn4']
    assert len(res.callables[0].args) == 1
    assert res.callables[0].args[0].name == 'number'

    assert len(res.callables[3].args) == 2
    assert res.callables[3].args[0].name == 'arg1'
    assert res.callables[3].args[1].name == 'arg2'
    assert res.callables[3].args[1].default == 5
