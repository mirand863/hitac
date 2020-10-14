from setuptools import setup, find_packages
import versioneer

setup(
    name="q2-hitac",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    packages=find_packages(),
    author="Fabio Malcher Miranda",
    author_email="fabio.malchermiranda@hpi.de",
    description="Hierarchical taxonomic classification",
    license='GPLv3',
    url="https://gitlab.com/dacs-hpi/hitac",
    entry_points={
        'qiime2.plugins':
        ['q2-hitac=q2_hitac.plugin_setup:plugin']
    },
    package_data={'q2_hitac': ['citations.bib']},
    zip_safe=False,
)
