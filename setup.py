from setuptools import setup, find_packages
import versioneer

import os

thelibFolder = os.path.dirname(os.path.realpath(__file__))
requirementPath = thelibFolder + '/requirements.txt'
install_requires = []
if os.path.isfile(requirementPath):
    with open(requirementPath) as f:
        install_requires = f.read().splitlines()

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="hitac",
    install_requires=install_requires,
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    author="Fabio Malcher Miranda",
    author_email="fabio.malchermiranda@hpi.de",
    description="Hierarchical taxonomic classifier",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    url="https://gitlab.com/dacs-hpi/hitac",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'qiime2.plugins':
        ['hitac=q2_hitac.plugin_setup:plugin']
    },
    package_data={'q2_hitac': ['citations.bib']},
    zip_safe=False,
    python_requires='>=3'
)
