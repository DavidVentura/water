import enum
import inspect
import re
import shlex

from dataclasses import dataclass
from typing import List, Dict, Callable, Any, Tuple, Optional, Union, NewType

class Flag:
    def __init__(self, checked):
        self.checked = checked

    def __bool__(self):
        return self.checked

def typing_get_args(a):
    return getattr(a, '__args__', None)

def typing_get_origin(a):
    return getattr(a, '__origin__', a)


class BadArguments(ValueError):
    pass


@dataclass
class MCallable:
    name: str
    args: List[inspect.Parameter]
    fn: Callable
    parent: 'Namespace'

    @staticmethod
    def from_callable(callable_root, name, parent) -> 'MCallable':
        s = inspect.signature(callable_root)
        return MCallable(name=name,
                         args=list(s.parameters.values()),
                         fn=callable_root,
                         parent=parent)


@dataclass
class Namespace:
    name: str
    members: List['Namespace']
    callables: List[MCallable]
    parent: Optional['Namespace'] = None

    @staticmethod
    def from_callable(callable_root, name=None, parent=None) -> 'Namespace':
        if not name:
            name = callable_root.__name__
        if inspect.isclass(callable_root):
            callable_root = callable_root()

        _is_mod = inspect.ismodule(callable_root)

        _members = inspect.getmembers(callable_root, lambda x: inspect.isclass(x) or (not _is_mod and inspect.ismodule(x)))
        _methods = inspect.getmembers(callable_root, lambda x: inspect.ismethod(x) or inspect.isfunction(x))

        ns = Namespace(name=name, members=[], callables=[], parent=parent)

        members = [Namespace.from_callable(_type, name, parent=ns) for name, _type in _members if not name.startswith('_')]
        methods = [MCallable.from_callable(_type, name, parent=ns) for name, _type in _methods]

        ns.members = members
        ns.callables = methods

        return ns


def args_to_kwargs(args: List[str]) -> Dict[str, Any]:
    kwargs = {}

    i = 0
    last_key = None
    while i < len(args):
        arg = args[i]
        if not arg.startswith('--') and last_key is None:
            raise BadArguments(f'Argument {arg} is neither a key (--option) nor a value')

        with_equal = re.match(r'(?P<flag>--[a-z0-9-_]+)=(?P<value>.+)', arg)
        if with_equal:
            k = with_equal.group('flag')
            v = with_equal.group('value')
            k = k[2:]  # '--a' -> 'a'
            k = k.replace('-', '_')  # '--a-thing' -> 'a_thing'
            kwargs[k] = v
        elif arg.startswith('--'):
            k = arg
            k = k[2:]  # '--a' -> 'a'
            k = k.replace('-', '_')  # '--a-thing' -> 'a_thing'
            kwargs[k] = None  # This enables 'flags' with no value
            last_key = k
        else:
            kwargs[last_key] = arg
            last_key = None
        i += 1
    return kwargs


def _parse(ns: Namespace, input_tokens: List[str]) -> Tuple[MCallable, Dict[str, Any]]:
    command, *args = input_tokens

    _members = {m.name: m for m in ns.members}
    if command in _members:
        return _parse(_members[command], args)

    _callables = {c.name: c for c in ns.callables}
    if command not in _callables:
        hierarchy = []
        parent = ns.parent
        while parent:
            hierarchy.insert(0, parent.name)
            parent = parent.parent
        _hierarchy = ' '.join(hierarchy[1:]) + ' '

        raise BadArguments(f"'{_hierarchy}{ns.name}' has no sub-command '{command}'")

    _callable = _callables[command]
    kwargs = args_to_kwargs(args)

    for a in _callable.args:
        if a.annotation == Flag:
            if a.name in kwargs:
                kwargs[a.name] = Flag(True)
            else:
                kwargs[a.name] = Flag(False)

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
    origin = typing_get_origin(annotation)
    args = typing_get_args(annotation)
    if origin == Union:
        for arg in args:
            try:
                value = cast(value, arg)
                break
            except Exception:
                continue
    elif origin in [list, tuple, List, Tuple]:
        value = value.split(',')
        if len(args):
            value = [cast(i, args[0]) for i in value]
    elif annotation in [int, float]:
        value = annotation(value)
    elif annotation is bool:
        value = value.lower() in ['true', '1', 't', 'y', 'yes']
    elif issubclass(annotation, enum.Enum):
        value = annotation[value]
    return value

def execute_command(c, input_command: str):
    parsed, kwargs = parse(Namespace.from_callable(c), input_command)
    return apply_args(parsed, kwargs)
