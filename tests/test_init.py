"""Test that evallog installs and imports."""

import evallog


def test_version():
    assert isinstance(evallog.__version__, str)
