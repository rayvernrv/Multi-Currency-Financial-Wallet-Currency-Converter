import pytest
import sys


from unittest.mock import patch
from datetime import date
from project import date_format, currency, amount, type_

# Test date_format()
def test_date_valid():
    with patch('builtins.input', return_value="2024-07-28"):  # builtins.input mocks user's input
        assert date_format() == date(2024, 7, 28)

    with patch('builtins.input', return_value="2024-7-28"):  # without leading "0" for month
        assert date_format() == date(2024, 7, 28)


def test_date_invalid():
    with patch('builtins.input', side_effect=["2024/07/28", "2024-07-28"]):  # wrong date format
        with patch('builtins.print') as mocked_print:  # builtins.print mocks the printing of ValueError
            assert date_format() == date(2024, 7, 28)
            mocked_print.assert_called_with("\nInvalid date.")

    with patch('builtins.input', side_effect=["2024-07-32", "2024-07-28"]):  # out of range date for July
        with patch('builtins.print') as mocked_print:
            assert date_format() == date(2024, 7, 28)
            mocked_print.assert_called_with("\nInvalid date.")

    with patch('builtins.input', side_effect=["foo", "2024-07-28"]):  # user inputted string
        with patch('builtins.print') as mocked_print:
            assert date_format() == date(2024, 7, 28)
            mocked_print.assert_called_with("\nInvalid date.")


# Test currency()
def test_currency_sgd():
    with patch('builtins.input', return_value="SGD"):
        assert currency() == "SGD"

    with patch('builtins.input', return_value="sgd"):  # test lower case input
        assert currency() == "SGD"


def test_currency_usd():
    with patch('builtins.input', return_value="USD"):
        assert currency() == "USD"

    with patch('builtins.input', side_effect=["GBP", "USD"]):  # invalid currency
        assert currency() == "USD"


def test_currency_eur():
    with patch('builtins.input', return_value="EUR"):
        assert currency() == "EUR"

    with patch('builtins.input', side_effect=["GBP", "EUR"]):
        with patch('builtins.print') as mocked_print:
            assert currency() == "EUR"
            mocked_print.assert_called_with("\nInvalid currency.\n")


# Test amount()
def test_amount_valid():
    with patch('builtins.input', return_value="10"):
        assert amount() == "10.00"

    with patch('builtins.input', return_value="12.3"):
        assert amount() == "12.30"

    with patch('builtins.input', return_value="12.34"):
        assert amount() == "12.34"

def test_amount_invalid():
    # negative amount, press "R" to re-enter amount
    with patch('builtins.input', side_effect=["-10", "R", "100"]):
        assert amount() == "100.00"

    with patch('builtins.input', side_effect=["foo", "100"]):  # user inputted string
        with patch('builtins.print') as mocked_print:
            assert amount() == "100.00"
            mocked_print.assert_called_with("\nInvalid input. Please input the amount in numeric format.\n")

    # negative amount, press any key to quit
    with patch('builtins.input', side_effect=["-10", "Q"]):
        with pytest.raises(SystemExit):
            amount()


# Test type_()
def test_type_income():
    with patch('builtins.input', return_value="I"):
        assert type_() == "Income"

    with patch('builtins.input', return_value="Income"):
        assert type_() == "Income"

    with patch('builtins.input', return_value="i"):  # test lower case input
        assert type_() == "Income"

    with patch('builtins.input', return_value="income"):
        assert type_() == "Income"


def test_type_expense():
    with patch('builtins.input', return_value="E"):
        assert type_() == "Expense"

    with patch('builtins.input', side_effect=["foo", "E"]):
        assert type_() == "Expense"

    with patch('builtins.input', side_effect=["foo", "E"]):  # user inputted string
        with patch('builtins.print') as mocked_print:
            assert type_() == "Expense"
            mocked_print.assert_called_with('\nInvalid input. Press "I" for Income or "E" for Expense.\n')
