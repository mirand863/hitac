"""QIIME2 public functions for HiTaC."""
from multiprocessing import cpu_count

import pandas as pd
import skbio
from hiclass import LocalClassifierPerLevel, LocalClassifierPerParent
from q2_types.feature_data import (
    DNAFASTAFormat,
    DNAIterator,
    FeatureData,
    Sequence,
    Taxonomy,
)
from qiime2.plugin import Float, Int
from sklearn.linear_model import LogisticRegression

from ._hierarchical_taxonomic_classifier import HierarchicalTaxonomicClassifier
from ._utils import (
    _extract_reads,
    compute_confidence,
    compute_frequencies,
    compute_possible_kmers,
    convert_taxonomy_to_qiime2,
    extract_qiime2_taxonomy,
)
from .plugin_setup import citations, plugin


def fit(
    reference_reads: DNAIterator,
    reference_taxonomy: pd.Series,
    kmer: int = 6,
    threads: int = cpu_count(),
) -> LocalClassifierPerParent:
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
    hierarchical_classifier : LocalClassifierPerParent
        Local hierarchical classifier based on the taxonomic hierarchy.
    """
    kmers = compute_possible_kmers(kmer)
    _, training_sequences = _extract_reads(reference_reads)
    X_train = compute_frequencies(training_sequences, kmers, threads)
    Y_train = extract_qiime2_taxonomy(reference_taxonomy)
    logistic_regression = LogisticRegression(
        solver="liblinear",
        multi_class="auto",
        class_weight="balanced",
        max_iter=10000,
        verbose=0,
        n_jobs=1,
    )
    hierarchical_classifier = LocalClassifierPerParent(
        local_classifier=logistic_regression, n_jobs=threads
    )
    hierarchical_classifier.fit(X_train, Y_train)
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


def classify(
    reads: DNAFASTAFormat,
    classifier: LocalClassifierPerParent,
    kmer: int = 6,
    threads: int = cpu_count(),
) -> pd.DataFrame:
    """
    Classify sequences with HiTaC.

    Parameters
    ----------
    reads : DNAFASTAFormat
        Reads to classify.
    classifier : LocalClassifierPerParent
        Pre-fitted hierarchical classifier.
    kmer : int, default=6
        K-mer size.
    threads : int, default='All CPUs'
        Number of threads for parallel classification.

    Returns
    -------
    classification : pd.DataFrame
        DataFrame containing the taxonomies assigned to each sequence.
    """
    kmers = compute_possible_kmers(kmer)
    # transform reads to DNAIterator
    reads = DNAIterator(skbio.read(str(reads), format="fasta", constructor=skbio.DNA))
    seq_ids, test_sequences = _extract_reads(reads)
    X_test = compute_frequencies(test_sequences, kmers, threads)
    predictions = classifier.predict(X_test)
    taxonomy = convert_taxonomy_to_qiime2(predictions)
    confidence = [-1] * len(seq_ids)
    result = pd.DataFrame(
        {"Taxon": taxonomy, "Confidence": confidence},
        index=seq_ids,
        columns=["Taxon", "Confidence"],
    )
    result.index.name = "Feature ID"
    return result


plugin.methods.register_function(
    function=classify,
    inputs={
        "reads": FeatureData[Sequence],
        "classifier": HierarchicalTaxonomicClassifier,
    },
    input_descriptions={
        "reads": "The feature data to be classified.",
        "classifier": "The hierarchical taxonomic classifier for classifying the reads.",
    },
    parameters={"kmer": Int, "threads": Int},
    parameter_descriptions={
        "kmer": "K-mer size.",
        "threads": "Number of threads for parallel classification",
    },
    outputs=[("classification", FeatureData[Taxonomy])],
    name="Hierarchical classification with HiTaC's pre-fitted model",
    description="Classify reads by taxon using a fitted hierarchical classifier.",
    citations=[citations["miranda2020hitac"]],
)


def fit_filter(
    reference_reads: DNAIterator,
    reference_taxonomy: pd.Series,
    kmer: int = 6,
    threads: int = cpu_count(),
) -> LocalClassifierPerLevel:
    """
    Fit HiTaC's filter.

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
    hierarchical_classifier : LocalClassifierPerLevel
        Local hierarchical filter based on the taxonomic hierarchy.
    """
    kmers = compute_possible_kmers(kmer)
    _, training_sequences = _extract_reads(reference_reads)
    X_train = compute_frequencies(training_sequences, kmers, threads)
    Y_train = extract_qiime2_taxonomy(reference_taxonomy)
    logistic_regression = LogisticRegression(
        solver="liblinear",
        multi_class="auto",
        class_weight="balanced",
        max_iter=10000,
        verbose=0,
        n_jobs=1,
    )
    hierarchical_classifier = LocalClassifierPerLevel(
        local_classifier=logistic_regression, n_jobs=threads
    )
    hierarchical_classifier.fit(X_train, Y_train)
    return hierarchical_classifier


plugin.methods.register_function(
    function=fit_filter,
    inputs={
        "reference_reads": FeatureData[Sequence],
        "reference_taxonomy": FeatureData[Taxonomy],
    },
    parameters={"kmer": Int, "threads": Int},
    parameter_descriptions={
        "kmer": "K-mer size.",
        "threads": "Number of threads for parallel training",
    },
    outputs=[("filter", HierarchicalTaxonomicClassifier)],
    name="Train HiTaC's hierarchical filter",
    description="Train HiTaC's hierarchical filter",
    citations=[citations["miranda2020hitac"]],
)


def filter(
    reads: DNAFASTAFormat,
    filter: LocalClassifierPerLevel,
    classification: pd.DataFrame,
    threshold: float = 0.7,
    kmer: int = 6,
    threads: int = cpu_count(),
) -> pd.DataFrame:
    """
    Filter sequences with HiTaC.

    Parameters
    ----------
    reads : DNAFASTAFormat
        Reads to filter.
    filter : LocalClassifierPerLevel
        Pre-fitted hierarchical filter.
    classification : pd.DataFrame
        Predictions made by HiTaC's classifier.
    threshold : float, default=0.7
        Confidence threshold for limiting taxonomic depth. Set to 0 to compute confidence score but not apply it to limit the taxonomic depth of the assignments.
    kmer : int, default=6
        K-mer size.
    threads : int, default='All CPUs'
        Number of threads for parallel filtering.

    Returns
    -------
    filtered_classification : pd.DataFrame
        DataFrame containing the taxonomies assigned to each sequence and the prediction probability for the lowest taxonomic rank.
    """
    kmers = compute_possible_kmers(kmer)
    # transform reads to DNAIterator
    reads = DNAIterator(skbio.read(str(reads), format="fasta", constructor=skbio.DNA))
    seq_ids, test_sequences = _extract_reads(reads)
    X_test = compute_frequencies(test_sequences, kmers, threads)
    predict_proba = filter.predict_proba(X_test)
    classes = filter.classes_
    classification = extract_qiime2_taxonomy(classification["Taxon"])
    predictions, confidence = compute_confidence(
        classification, classes, predict_proba, threshold
    )
    taxonomy = convert_taxonomy_to_qiime2(predictions)
    result = pd.DataFrame(
        {"Taxon": taxonomy, "Confidence": confidence},
        index=seq_ids,
        columns=["Taxon", "Confidence"],
    )
    result.index.name = "Feature ID"
    return result


plugin.methods.register_function(
    function=filter,
    inputs={
        "reads": FeatureData[Sequence],
        "filter": HierarchicalTaxonomicClassifier,
        "classification": FeatureData[Taxonomy],
    },
    input_descriptions={
        "reads": "The feature data to be filtered.",
        "filter": "The hierarchical taxonomic filter for filtering the reads.",
        "classification": "The predictions made by HiTaC",
    },
    parameters={"threshold": Float, "kmer": Int, "threads": Int},
    parameter_descriptions={
        "threshold": "Confidence threshold for limiting taxonomic depth. Set to 0 to compute confidence score but not apply it to limit the taxonomic depth of the assignments.",
        "kmer": "K-mer size.",
        "threads": "Number of threads for parallel filtering",
    },
    outputs=[("filtered_classification", FeatureData[Taxonomy])],
    name="Hierarchical classification filtering with HiTaC's pre-fitted model",
    description="Filter reads using a fitted hierarchical filter.",
    citations=[citations["miranda2020hitac"]],
)
