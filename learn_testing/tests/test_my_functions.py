import pytest
import sys
import os

# Calculate the absolute path to the project root
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.insert(0, project_root)  # Insert at the beginning of sys.path

from learn_testing.source.my_functions import add, divide

def test_add():
    result = add(1, 4)
    assert result == 5

def test_divide():
    result = divide(10, 5)
    assert result == 2

def test_divide_zero():
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)

def test_add_strings():
    result = add("I like ", "coffee")
    assert result == "I like coffee"
    