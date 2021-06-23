# Integration with documentation

## Integrating into documentation generation

Included in the `helpers` module there's a `generate_docs` function, that is both 
a valid starting point and a decently usable way to generate "default" documentation.

It is a _starting point_ because every project's documentation is different and you 
most likely want to customize it.

```
{%
   include-markdown "a.py"
   comments=false
%}
```

You can see the generated output [here](example.md)



## Integrating into documentation testing

As an example of the power you get from being able to run the command 
parser, we can look into parsing documentation and validating every executed command.

Our sample docs:

```markdown
Example docs that could be automatically tested:

# Commands

> add --a 1 --b 2
> add --a 1
> add --a 1 --b some_string
```

And the tests for the docs
```python
import pytest

from water_cli.parser import Namespace, parse_examples, cast

class c:
    pass

ns = Namespace.from_callable(c)

@pytest.mark.parametrize('line', docs.readlines())
def test_docs(line):
    # test that every _present_ example on every command passes type checking
    # and that the name in the example matches the argument of the function
    examples_by_arg = parse_examples(parsed_doc.meta)
    args_by_name = {a.name: a for a in command.args}

    for k, v in examples_by_arg.items():
        cast(v, args_by_name[k].annotation)

```

