import pytest
import sys
import os

# Calculate the absolute path to the project root
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.insert(0, project_root)  # Insert at the beginning of sys.path

from learn_testing.source.my_functions import add

def test_add():
    pass
