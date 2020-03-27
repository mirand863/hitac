#!/usr/bin/env python3

import setuptools
import os

thelibFolder = os.path.dirname(os.path.realpath(__file__))
requirementPath = thelibFolder + '/requirements.txt'
install_requires = []
if os.path.isfile(requirementPath):
    with open(requirementPath) as f:
        install_requires = f.read().splitlines()

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hitac",
    install_requires=install_requires,
    version="1.0",
    author="Fabio Malcher Miranda",
    author_email="fabio.malchermiranda@hpi.de",
    description="A hierarchical taxonomy classifier for fungal ITS sequences",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/dacs-hpi/hitac",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3',
)


