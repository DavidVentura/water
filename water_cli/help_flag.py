import inspect
from typing import Callable, TypeVar, Concatenate, ParamSpec, Optional, cast, Any
from functools import update_wrapper
from water_cli.parser import HelpType

R = TypeVar('R')
P = ParamSpec('P')

def add_help_flag(fn: Callable[P, R]) -> Callable[Concatenate[HelpType, P], R]:
    assert hasattr(fn, '__doc__'), f'Expected {fn} to have __doc__'
    assert hasattr(fn, '__name__'), f'Expected {fn} to have __name__'
    assert fn.__doc__ is not None, f'Expected {fn.__name__} to have non-null __doc__'
    assert fn.__doc__.strip() != '', f'Expected {fn.__name__} to have non-empty __doc__'

    s = inspect.signature(fn)

    # https://github.com/python/mypy/issues/13711
    # named arguments _must_ be positional only in this situation
    #def _inner(*args: P.args, help: Optional[HelpType]=None, **kwargs: P.kwargs) -> R:
    def _inner(help: Optional[HelpType]=None, /, *args: P.args, **kwargs: P.kwargs) -> R:
        print()
        print('##' * 50)
        print(s, _s)
        print(_inner.__signature__)
        print(help, args, kwargs)
        print('##' * 50)
        if not isinstance(help, HelpType):
            args = (help,) + args
        return fn(*args, **kwargs)

    update_wrapper(_inner, fn)
    _s = inspect.signature(_inner)
    params = list(s.parameters.values())
    params.append(inspect.Parameter("help", inspect.Parameter.KEYWORD_ONLY, annotation=HelpType, default=None))
    _inner.__signature__ = s.replace(parameters=params)  # type: ignore
    #_inner.__doc__ = fn.__doc__
    return cast(Callable[Concatenate[HelpType, P], R], _inner)
