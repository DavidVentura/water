import tempfile
import subprocess
import shlex
import glob

import pytest

from dataclasses import dataclass
from typing import List, Tuple

from black import format_str, FileMode
from mistletoe import Document
from mistletoe.block_token import CodeFence, Heading
from mistletoe.span_token import RawText, InlineCode

@dataclass
class RunScript:
    args: List[str]
    combined_output: str

@dataclass
class ExampleWithArgs:
    src: str
    run_scripts: List[RunScript]
    heading: str

def _parse_run_script(script: str) -> List[RunScript]:
    """
    $ python example.py command --arg value
    You ran "command" with arg="value"
    $ python example.py command2 --arg value2
    You ran "command2" with arg="value2"
    ->
    [RunScript(['command', '--arg', 'value'], 'You ran "command" with arg="value"'),
     RunScript(['command2', '--arg', 'value2'], 'You ran "command2" with arg="value2"'),
     ]
    """

    results = []
    cur_args = []
    cur_output = []

    for line in script.splitlines():
        line = line.strip()
        if line.startswith('$'):
            if cur_args:
                results.append(RunScript(cur_args, '\n'.join(cur_output)))
                cur_args = []
                cur_output = []

            args = shlex.split(line)
            assert args[0] == '$'
            assert args[1] == 'python'
            cur_args = args[3:]
            continue
        cur_output.append(line)

    if cur_args:
        results.append(RunScript(cur_args, '\n'.join(cur_output)))

    assert len(results) > 0, f'Could not parse any script out of {script}'

    return results


def _get_examples_and_args_from_fd(f) -> List[ExampleWithArgs]:
    d = Document(f)
    code_blocks = [c for c in d.children if isinstance(c, CodeFence)]
    examples_and_args: List[ExampleWithArgs] = []

    _last_py_codeblock = None
    _last_heading = None
    for (i, b) in enumerate(d.children):
        if isinstance(b, CodeFence):
            if b.language != 'run_example':
                continue
            assert i > 0, "Can't have run_example as first block"
            for _i in range(i, -1, -1):
                _this_child = d.children[_i]
                if isinstance(_this_child, CodeFence) and _this_child.language == 'python':
                    _last_py_codeblock = _this_child
                    break
            assert _last_py_codeblock, "There's no `python` block precursor to this `run_example`"
            assert _last_heading, "The codeblock must always be preceded by a heading"

            assert len(_last_py_codeblock.children) == 1
            assert len(b.children) == 1

            # per internal mistletoe contract
            assert isinstance(_last_py_codeblock.children[0], RawText)
            assert isinstance(b.children[0], RawText)


            cmdline = b.children[0].content
            e = ExampleWithArgs(_last_py_codeblock.children[0].content, _parse_run_script(cmdline), _last_heading)
            examples_and_args.append(e)
        elif isinstance(b, Heading):
            _str = ''
            for _child in b.children:
                if isinstance(_child, InlineCode):
                    _str += _child.children[0].content
                else:
                    _str += _child.content
            _last_heading = '_'.join(_str.split()).lower()


    return examples_and_args


def _parse(fnames: List[str]) -> List[ExampleWithArgs]:
    ret = []
    for filename in fnames:
        with open(filename, 'r') as f:
            examples = _get_examples_and_args_from_fd(f)
        for example in examples:
            ret.append(pytest.param(example, id=f'{filename}_{example.heading}'))
    return ret


@pytest.mark.parametrize('example', _parse(glob.glob('docs/uti*.md')))
def test_python_code_blocks_execute_with_bash_arguments(example):
    with tempfile.NamedTemporaryFile(mode='w') as ntf:
        ntf.write(example.src)
        ntf.flush()
        for invocation in example.run_scripts:
            cmd = ["python", ntf.name] + invocation.args
            s = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout = s.stdout.decode('utf-8').strip()
            stderr = s.stderr.decode('utf-8').strip()
            combined = stdout + stderr
            assert combined == invocation.combined_output


@pytest.mark.parametrize('example', _parse(glob.glob('docs/*.md')))
def test_python_code_blocks_are_linted(example):
    res = format_str(example.src, mode=FileMode())
    assert res == example.src
