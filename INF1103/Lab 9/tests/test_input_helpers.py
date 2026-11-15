"""
Section 5.1: invalid user input is handled without crashing, and the user
is asked again. monkeypatch replaces input() so the test can "type" answers;
capsys captures what was printed.
"""

from inventory_manager import get_non_negative_int, get_positive_float


def fake_input(monkeypatch, answers: list[str]) -> None:
    """Makes input() return the next answer each time it is called."""
    remaining = iter(answers)
    monkeypatch.setattr("builtins.input", lambda prompt="": next(remaining))


def test_get_positive_float_returns_valid_value(monkeypatch, capsys):
    fake_input(monkeypatch, ["12.50"])
    assert get_positive_float("Price: ") == 12.5
    assert capsys.readouterr().out == ""


def test_get_positive_float_asks_again_until_valid(monkeypatch, capsys):
    fake_input(monkeypatch, ["abc", "-5", "12.50"])
    assert get_positive_float("Price: ") == 12.5

    printed = capsys.readouterr().out.splitlines()
    assert printed == ["Please enter a valid number, e.g. 12.50",
                       "Please enter a number greater than zero."]


def test_get_positive_float_rejects_zero(monkeypatch, capsys):
    fake_input(monkeypatch, ["0", "1"])
    assert get_positive_float("Price: ") == 1.0
    assert "greater than zero" in capsys.readouterr().out


def test_get_non_negative_int_asks_again_until_valid(monkeypatch, capsys):
    fake_input(monkeypatch, ["ten", "2.5", "-3", "0"])
    assert get_non_negative_int("Stock Quantity: ") == 0

    printed = capsys.readouterr().out.splitlines()
    assert printed == ["Please enter a valid whole number, e.g. 10",
                       "Please enter a valid whole number, e.g. 10",
                       "Please enter a whole number that is zero or more."]
