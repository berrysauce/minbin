"""
app/utils/other.py

Utility functions for the application.
"""

import toml


def get_version():
    """
    Get the version of the application from pyproject.toml.
    """
    # Load the pyproject.toml file and return the version
    pyproject = toml.load("pyproject.toml")
    return pyproject["project"]["version"]
