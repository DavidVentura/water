import sys
from examples import calculator
from water_cli import simple_cli
from unittest.mock import patch


def test_simple_cli_no_command(capsys):
    with patch("sys.argv", [sys.argv[0], "asd"]):
        simple_cli(calculator.Calculator)
    captured = capsys.readouterr()
    assert captured.out.strip() == "No top-level command 'asd'. Try any of: ['double']"


def test_simple_cli_bad_argument_command(capsys):
    with patch("sys.argv", [sys.argv[0], "double", "--number", "banana"]):
        simple_cli(calculator.Calculator)
    captured = capsys.readouterr()
    assert captured.out.strip() == "Unable to convert 'banana' to type 'int': invalid literal for int() with base 10: 'banana'"


def test_simple_cli_ok_command(capsys):
    with patch("sys.argv", [sys.argv[0], "double", "--number", "10"]):
        simple_cli(calculator.Calculator)
    captured = capsys.readouterr()
    assert captured.out.strip() == "20"
