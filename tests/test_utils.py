import pytest

from typing import Optional
from water_cli.parser import Flag
from water_cli.utils import exclusive_flags, required_together
from water_cli.exceptions import ExclusiveFlags, MissingRequiredCombination

@exclusive_flags([("a", "b")])
def f(*, a: Optional[str] = None, b: Optional[str] = None):
    pass

@exclusive_flags([("a", "b")])
def f_flag(*, a: Flag, b: Flag):
    pass

def test_exclusive_no_conflict():
    f(a="a")
    f(b="b")
    f()

def test_exclusive_conflict():
    with pytest.raises(ExclusiveFlags) as e:
        f(a="a", b="b")
    assert e.value.exclusive_flags == ('a' , 'b')

def test_exclusive_flag_no_conflict():
    f_flag(a=Flag(False), b=Flag(False))
    f_flag(a=Flag(True), b=Flag(False))
    f_flag(a=Flag(False), b=Flag(True))

def test_exclusive_flag_conflict():
    with pytest.raises(ExclusiveFlags) as e:
        f_flag(a=Flag(True), b=Flag(True))
    assert e.value.exclusive_flags == ('a' , 'b')

@required_together([("a", "b")])
def required_1(*, a: Optional[str] = None, b: Optional[str] = None):
    pass

@required_together([("a", "b")])
def required_2(*, a: Flag, b: Flag):
    pass

@required_together([("a", "b"), ("c", "d")])
def required_3(*, a: Flag, b: Flag, c: Flag, d: Flag):
    pass

def test_required_together_provided():
    required_1(a="a", b="b")

def test_required_together_not_provided():
    required_1()

def test_required_together_missing():
    with pytest.raises(MissingRequiredCombination) as e:
        required_1(a="a")
    assert e.value.present_flags == ('a',)
    assert e.value.required_combination == ('b',)
    assert str(e.value) == "Passing the flags --a also requires the flags: --b to be provided"

    with pytest.raises(MissingRequiredCombination) as e:
        required_1(b="b")
    assert e.value.present_flags == ('b',)
    assert e.value.required_combination == ('a',)
    assert str(e.value) == "Passing the flags --b also requires the flags: --a to be provided"

def test_required_together_not_provided_flags():
    required_2(a=Flag(False), b=Flag(False))
    required_3(a=Flag(False), b=Flag(False), c=Flag(False), d=Flag(False))

def test_required_together_provided_flags():
    required_2(a=Flag(True), b=Flag(True))

def test_required_together_missing_flags():
    with pytest.raises(MissingRequiredCombination) as e:
        required_2(a=Flag(True), b=Flag(False))
    assert e.value.present_flags == ('a',)
    assert e.value.required_combination == ('b',)
    assert str(e.value) == "Passing the flags --a also requires the flags: --b to be provided"

    with pytest.raises(MissingRequiredCombination) as e:
        required_2(a=Flag(False), b=Flag(True))
    assert e.value.present_flags == ('b',)
    assert e.value.required_combination == ('a',)
    assert str(e.value) == "Passing the flags --b also requires the flags: --a to be provided"


@pytest.mark.parametrize("decorator", [(required_together), (exclusive_flags)])
def test_passing_bad_decorator_arguments(decorator):
    with pytest.raises(ValueError) as e:
        @decorator([("a", "b"), ("c", "d")])
        def a_function(*, a: Flag, b: Flag):
            pass
    assert str(e.value) == f"Received arguments: ('c', 'd') for decorator, which are not accepted by 'a_function'."
