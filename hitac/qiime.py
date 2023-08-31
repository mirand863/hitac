"""QIIME2 public functions for HiTaC."""
from multiprocessing import cpu_count

import pandas as pd
from hiclass import LocalClassifierPerParentNode
from q2_types.feature_data import (
    DNAIterator,
    FeatureData,
    Sequence,
    Taxonomy,
)
from qiime2.plugin import Int
from sklearn.linear_model import LogisticRegression

from ._qiime import HierarchicalTaxonomicClassifier
from ._utils import (
    _extract_reads,
    extract_qiime2_taxonomy,
    compute_possible_kmers,
    compute_frequencies,
    get_hierarchical_classifier,
)
from .plugin_setup import citations, plugin


def fit(
    reference_reads: DNAIterator,
    reference_taxonomy: pd.Series,
    kmer: int = 6,
    threads: int = cpu_count(),
) -> LocalClassifierPerParentNode:
    """
    Fit HiTaC's classifier.

    Parameters
    ----------
    reference_reads : DNAIterator
        Reference reads.
    reference_taxonomy : pd.Series
        Reference taxonomy.
    kmer : int, default=6
        K-mer size.
    threads : int, default='All CPUs'
        Number of threads for parallel training.

    Returns
    -------
    hierarchical_classifier : LocalClassifierPerParentNode
        Local hierarchical classifier based on the taxonomic hierarchy.
    """
    kmers = compute_possible_kmers(kmer)
    _, training_sequences = _extract_reads(reference_reads)
    x_train = compute_frequencies(training_sequences, kmers, threads)
    y_train = extract_qiime2_taxonomy(reference_taxonomy)
    hierarchical_classifier = get_hierarchical_classifier(threads)
    hierarchical_classifier.fit(x_train, y_train)
    return hierarchical_classifier


plugin.methods.register_function(
    function=fit,
    inputs={
        "reference_reads": FeatureData[Sequence],
        "reference_taxonomy": FeatureData[Taxonomy],
    },
    parameters={"kmer": Int, "threads": Int},
    parameter_descriptions={
        "kmer": "K-mer size.",
        "threads": "Number of threads for parallel training",
    },
    outputs=[("classifier", HierarchicalTaxonomicClassifier)],
    name="Train HiTaC's hierarchical classifier",
    description="Train HiTaC's hierarchical classifier",
    citations=[citations["miranda2020hitac"]],
)
