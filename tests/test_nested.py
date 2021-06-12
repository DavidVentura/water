from water import __version__
from water.parser import Namespace


class NestedObj:
    class Inside1:
        def fn1(self, number):
            pass

    class Inside2:
        class ReallyInside:
            def fn2(self, *, number):
                pass

    def a(self):
        pass


def test_namespace():
    res = Namespace.from_callable(NestedObj)
    assert res.name == 'NestedObj'
    assert len(res.callables) == 1
    assert res.callables[0].name == 'a'

    assert len(res.members) == 2
    i1 = res.members[0]
    i2 = res.members[1]
    assert i1.name == 'Inside1'
    assert i2.name == 'Inside2'

    assert len(i1.callables) == 1
    assert i1.callables[0].fn.__name__ == 'fn1'
    assert i1.callables[0].fn.__self__.__class__ == NestedObj.Inside1

    assert len(i2.callables) == 0
    assert len(i2.members) == 1

    ri = i2.members[0]
    assert len(ri.callables) == 1
    assert ri.callables[0].fn.__name__ == 'fn2'
    assert ri.callables[0].fn.__self__.__class__ == NestedObj.Inside2.ReallyInside
