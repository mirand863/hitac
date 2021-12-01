"""Init module for the library."""
import importlib

from ._version import get_versions

__version__ = get_versions()["version"]
del get_versions

importlib.import_module("hitac.classifier")
