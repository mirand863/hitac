from ._classify import classify
from ._version import get_versions

__version__ = get_versions()['version']
del get_versions

__all__ = ['fit_classifier']

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
