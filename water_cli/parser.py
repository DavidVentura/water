import shlex
import inspect
import re
import typing

from dataclasses import dataclass
from typing import List, Dict, Callable, Any, Tuple

class BadArguments(ValueError):
    pass

@dataclass
class MCallable:
    name: str
    args: List[inspect.Parameter]
    fn: Callable

    @staticmethod
    def from_callable(callable_root, name) -> 'MCallable':
        s = inspect.signature(callable_root)
        return MCallable(name=name,
                         args=list(s.parameters.values()),
                         fn=callable_root)


@dataclass
class Namespace:
    name: str
    members: List['Namespace']
    callables: List[MCallable]

    @staticmethod
    def from_callable(callable_root, name=None) -> 'Namespace':
        if not name:
            name = callable_root.__name__
        if inspect.isclass(callable_root):
            callable_root = callable_root()
        _is_mod = inspect.ismodule(callable_root)

        _members = inspect.getmembers(callable_root, lambda x: inspect.isclass(x) or (not _is_mod and inspect.ismodule(x)))
        _methods = inspect.getmembers(callable_root, lambda x: inspect.ismethod(x) or inspect.isfunction(x))

        members = [Namespace.from_callable(_type, name) for name, _type in _members if not name.startswith('_')]
        methods = [MCallable.from_callable(_type, name) for name, _type in _methods]

        return Namespace(name=name, members=members, callables=methods)

def args_to_kwargs(args: List[str]) -> Dict[str, Any]:
    kwargs = {}

    i = 0
    while i < len(args):
        arg = args[i]
        if not arg.startswith('--'):
            raise BadArguments(f'Argument {arg} is neither a key (--option) nor a value')

        with_equal = re.match(r'(?P<flag>--[a-z0-9-_]+)=(?P<value>.+)', arg)
        if with_equal:
            k = with_equal.group('flag')
            v = with_equal.group('value')
        else:
            if i+1 == len(args):
                raise BadArguments(f'Flag {arg} missing value')
            k = arg
            v = args[i+1]
            i += 1

        k = k[2:]  # '--a' -> 'a'
        k = k.replace('-', '_')  # '--a-thing' -> 'a_thing'
        i += 1
        kwargs[k] = v
    return kwargs


def _parse(ns: Namespace, input_tokens: List[str]) -> Tuple[MCallable, Dict[str, Any]]:
    command, *args = input_tokens

    _members = {m.name: m for m in ns.members}
    if command in _members:
        return _parse(_members[command], args)

    _callables = {c.name: c for c in ns.callables}
    if command not in _callables:
        raise BadArguments(f"{ns} has no {command}")

    _callable = _callables[command]
    kwargs = args_to_kwargs(args)

    all_params = {a.name for a in _callable.args}
    needed_params = {a.name for a in _callable.args if a.default is inspect.Parameter.empty}
    rcvd_params = set(kwargs.keys())

    missing_params = needed_params - rcvd_params
    extra_params = rcvd_params - all_params
    if missing_params:
        raise BadArguments(f"No parameters for {missing_params}")
    elif extra_params:
        raise BadArguments(f"Too many parameters: {extra_params}")

    return _callable, kwargs


def parse(ns: Namespace, input_command: str) -> Tuple[MCallable, Dict[str, Any]]:
    return _parse(ns, shlex.split(input_command))


def apply_args(c: MCallable, kwargs: Dict[str, Any]) -> Any:
    casted = {}
    args_by_name = {a.name: a for a in c.args}
    for k, v in kwargs.items():
        casted[k] = cast(v, args_by_name[k].annotation)

    return c.fn(**casted)

def cast(value: Any, annotation: Any):
    origin = typing.get_origin(annotation)
    args = typing.get_args(annotation)
    # print(value, annotation, origin, args)
    if origin == typing.Union:
        for arg in args:
            try:
                value = cast(value, arg)
                break
            except Exception:
                continue
    elif origin in [list, tuple]:
        value = value.split(',')
        if len(args):
            value = [cast(i, args[0]) for i in value]
    elif annotation in [int, float]:
        value = annotation(value)
    elif annotation is bool:
        value = value.lower() in ['true', '1', 't', 'y', 'yes']
    return value

def execute_command(c, input_command: str):
    parsed, kwargs = parse(Namespace.from_callable(c), input_command)
    return apply_args(parsed, kwargs)
