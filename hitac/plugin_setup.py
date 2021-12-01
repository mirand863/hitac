"""QIIME2 plugin setup."""
from qiime2.plugin import Citations, Plugin

import hitac

citations = Citations.load("citations.bib", package="hitac")

plugin = Plugin(
    name="hitac",
    version=hitac.__version__,
    website="https://gitlab.com/dacs-hpi/hitac",
    package="hitac",
    description=(
        "This QIIME 2 plugin wraps HiTaC for hierarchical taxonomic classification."
    ),
    short_description="Plugin for hierarchical taxonomic classification.",
    citations=[citations["miranda2020hitac"]],
)
