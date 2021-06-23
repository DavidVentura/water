import inspect
import typing

from water_cli.parser import Namespace
try:
    from docstring_parser import parse
except ImportError:
    print('Install water_cli[docs] to use these features')
    raise


def generate_docs(ns: Namespace, heading: str = '##') -> str:
    lines = []
    for category, _commands in commands(ns).items():
        if not _commands:
            continue
        for c in _commands:
            lines.append(f'{heading} {c.name}')
            lines.extend(docs_for_command(c, category))
            lines.append('')
    return '\n'.join(lines)


def parse_examples(meta):
    """
    Parses the 'Examples:' section of a docstring into k-v pairs. Each arg must be exactly 1 line.

    '''
    ...
    Examples:
    arg1: something or other
    arg2: value2
    '''
    -> {'arg1': 'something or other', 'arg2': 'value2'}
    """
    data = ''
    for item in meta:
        if item.args != ['examples']:
            continue
        data = item.description
        break

    examples = {}
    for line in data.splitlines():
        key, _, value = line.partition(':')
        examples[key] = value.strip()
    return examples


def _unoptional(annot):
    origin = getattr(annot, '__origin__', annot)  # similar to typing.get_origin, which is not available til py3.7
    annot_args = getattr(annot, '__args__', None)
    if origin != typing.Union:
        return annot
    if len(annot_args) != 2:
        return annot

    if type(None) not in annot_args:
        return annot

    return [a for a in annot_args if a is not type(None)][0]  # flake8: noqa: E721


def show(what):
    for c in what.callables:
        if c.name.startswith('_'):
            continue
        yield c

    for m in what.members:
        yield from show(m)


def commands(ns: Namespace):
    commands_by_parent = {}
    for c in show(ns):
        parents = []
        _p = c.parent
        while _p:
            parents.insert(0, _p)
            _p = _p.parent
        parents = parents[1:]

        parent_commands = ' '.join([p.name for p in parents])
        commands_by_parent.setdefault(parent_commands, [])
        commands_by_parent[parent_commands].append(c)
    return commands_by_parent


def docs_for_command(c, category):
    lines = []
    parsed_doc = parse(c.fn.__doc__)
    if parsed_doc.short_description:
        lines.append(parsed_doc.short_description)
    if parsed_doc.long_description:
        lines.append(parsed_doc.long_description)
    lines.append('')
    lines.append('Example:')
    lines.append('```bash')

    params_by_name = {}
    line_args = ''
    args = sorted(c.args, key=lambda x: x.default == inspect.Parameter.empty, reverse=True)
    for arg in args:
        annot = _unoptional(arg.annotation)
        annot_name = getattr(annot, '__name__', annot)
        arg_fmt = f'--{arg.name} {annot_name}'
        if arg.default != inspect.Parameter.empty:
            arg_fmt = f'[{arg_fmt}]'
        line_args += f' {arg_fmt}'
        params_by_name[arg.name] = arg
    lines.append(f'{category} {c.name} {line_args}')
    lines.append('```')

    docs_by_arg = {param.arg_name: param for param in parsed_doc.params}
    lines.append('Arguments:')
    lines.append('')
    examples_by_arg = parse_examples(parsed_doc.meta)
    lines.append('|name|type|example|description|default|')
    lines.append('|----|----|-------|-----------|-------|')
    for arg_name, arg in params_by_name.items():
        param = docs_by_arg.get(arg.name)
        if param:
            desc = param.description.replace('\n', '<br/>')
        else:
            desc = '&nbsp;'
        default = arg.default if arg.default != inspect.Parameter.empty else '&nbsp;'

        annot = getattr(arg.annotation, '__name__', arg.annotation)
        annot = _unoptional(annot)
        annot = getattr(annot, '__name__', annot)
        example = examples_by_arg.get(arg_name) or ''

        lines.append(f'|{arg_name}|{annot}|{example}|{desc}|{default}|')
    lines.append('')
    return lines
