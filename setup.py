"""setup file for the project."""

# code gratefully take from https://github.com/navdeep-G/setup.py

# Note: To use the 'upload' functionality of this file, you must:
#   $ pipenv install twine --dev

import io
import os
import sys
import versioneer
from shutil import rmtree

from setuptools import find_packages, setup, Command

# Package meta-data.
NAME = "hitac"
DESCRIPTION = "Hierarchical taxonomic classifier."

# URL = 'https://gitlab.com/dacs-hpi/hitac'
# URL_DOKU = "https://gitlab.com/dacs-hpi/hitac
URL_GITHUB = "https://gitlab.com/dacs-hpi/hitac"
URL_ISSUES = "https://gitlab.com/dacs-hpi/hitac/-/issues"
EMAIL = "fabio.malchermiranda@hpi.de"
AUTHOR = "Fabio Malcher Miranda"
REQUIRES_PYTHON = ">=3.8"
KEYWORDS = ["hierarchical taxonomic classifier"]
DACS_SOFTWARE = "https://gitlab.com/dacs-hpi"
# What packages are required for this module to be executed?
REQUIRED = ["pandas", "numpy", "scikit-learn", "hiclass", "scikit-bio"]

# What packages are optional?
# 'fancy feature': ['django'],}
# EXTRAS = {"ray": ["ray>=1.11.0"]}
extras = dict()
extras["dev"] = [
    "pytest",
    "flake8",
    "pydocstyle",
    "pytest-cov",
    "pre-commit",
    "pyfakefs",
]

# The rest you shouldn't have to touch too much :)
# ------------------------------------------------
# Except, perhaps the License and Trove Classifiers!
# If you do change the License, remember to change the Trove Classifier for that!

here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
try:
    with io.open(os.path.join(here, "README.md"), encoding="utf-8") as f:
        long_description = "\n" + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

# Load the package's _version.py module as a dictionary.
about = {}
# project_slug = NAME.lower().replace("-", "_").replace(" ", "_")
project_slug = "hitac"
# with open(os.path.join(here, project_slug, '_version.py')) as f:
#    exec(f.read(), about)


class UploadCommand(Command):
    """Support setup.py upload."""

    description = "Build and publish the package."
    user_options = []

    @staticmethod
    def status(s):
        """Print things in bold."""
        print("\033[1m{0}\033[0m".format(s))

    def initialize_options(self):
        """Init options."""
        pass

    def finalize_options(self):
        """Finalize method."""
        pass

    def run(self):
        """Run method."""
        try:
            self.status("Removing previous builds…")
            rmtree(os.path.join(here, "dist"))
        except OSError:
            pass

        self.status("Building Source and Wheel (universal) distribution…")
        os.system("{0} setup.py sdist bdist_wheel --universal".format(sys.executable))

        self.status("Uploading the package to PyPI via Twine…")
        os.system("twine upload dist/*")

        self.status("Pushing git tags…")
        os.system("git tag v{0}".format(about["__version__"]))
        os.system("git push --tags")

        sys.exit()


# Where the magic happens:
setup(
    name=NAME,
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    project_urls={
        "Bug Tracker": URL_ISSUES,
        "Source Code": URL_GITHUB,
        # "Documentation": URL_DOKU,
        # "Homepage": URL,
        "Related Software": DACS_SOFTWARE,
    },
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    entry_points={
        "qiime2.plugins": ["hitac=hitac.plugin_setup:plugin"],
        "console_scripts": [
            "hitac-fit=hitac.hitac_fit:main",
            "hitac-classify=hitac.hitac_classify:main",
            "hitac-fit-filter=hitac.hitac_fit_filter:main",
            "hitac-filter=hitac.hitac_filter:main",
        ],
    },
    package_data={"hitac": ["citations.bib"]},
    install_requires=REQUIRED,
    extras_require=extras,
    include_package_data=True,
    license="BSD 3-Clause",
    keywords=KEYWORDS,
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: PyPy",
        "License :: OSI Approved",
    ],
)
#    # $ setup.py publish support.
#    cmdclass={
#        'upload': UploadCommand,
#    },
