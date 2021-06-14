import enum
import typing

import pytest

from water_cli.parser import cast

class SomeEnum(enum.Enum):
    SOMETHING = enum.auto()
    OTHER = enum.auto()


@pytest.mark.parametrize('_type,in_str,expected', [
    (str, "some string", "some string"),
    (int, "10", 10),

    (bool, "1", True),
    (bool, "yes", True),
    (bool, "true", True),
    (bool, "True", True),
    (bool, "T", True),

    (bool, "0", False),
    (bool, "no", False),
    (bool, "false", False),
    (bool, "False", False),
    (bool, "F", False),
    (bool, "something weird", False),

    (typing.List[str], "10", ["10"]),
    (typing.List[int], "10", [10]),

    (typing.List[str], "10,20,30", ["10", "20", "30"]),
    (typing.List[int], "10,20,30", [10, 20, 30]),

    (typing.List[str], "10.5,20.5,30.5", ["10.5", "20.5", "30.5"]),
    (typing.List[float], "10.5,20.5,30.5", [10.5, 20.5, 30.5]),

    (typing.Optional[str], "asd", "asd"),
    (typing.Optional[str], None, None),

    (typing.Optional[typing.List[str]], "asd", ["asd"]),
    (typing.Optional[typing.List[str]], None, None),
    (typing.Optional[typing.List[str]], None, None),

    (SomeEnum, 'SOMETHING', SomeEnum.SOMETHING),
    (SomeEnum, 'OTHER', SomeEnum.OTHER),
    ])
def test_cast(_type, in_str, expected):
    assert cast(in_str, _type) == expected
