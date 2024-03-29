"""Helper functions for data manipulation."""

import concurrent.futures
import itertools
import logging
from itertools import product
from multiprocessing import cpu_count

import numpy as np
from hiclass import LocalClassifierPerParentNode
from sklearn.linear_model import LogisticRegression
from typing import List, TextIO

from hitac.filter import Filter


# Create logger
logger = logging.getLogger("HiTaC")
logger.setLevel(5)

# Create console handler and set verbose level
if not logger.hasHandlers():
    ch = logging.StreamHandler()
    ch.setLevel(5)

    # Create formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Add formatter to ch
    ch.setFormatter(formatter)

    # Add ch to logger
    logger.addHandler(ch)


def compute_possible_kmers(kmer_size: int = 6, alphabet: str = "ACGT") -> np.ndarray:
    """
    Compute all kmer possibilities based on given alphabet.

    Parameters
    ----------
    kmer_size : int, default=6
        K-mer size.
    alphabet : str, default='ACGT'
        The alphabet used to compute k-mers.

    Returns
    -------
    kmers : np.ndarray
        Numpy array containing all possible k-mers.
    """
    logger.info("Computing possible k-mers")
    kmers = ["".join(c) for c in product(alphabet, repeat=kmer_size)]
    return np.array(kmers)


def compute_kmer_frequency(sequence: str, kmers: list) -> np.array:
    """
    Compute kmer frequencies for a given sequence.

    Parameters
    ----------
    sequence : str
        Sequence to compute k-mer frequency.
    kmers : list
        List containing possible k-mers to compute frequency (anything else is not counted).

    Returns
    -------
    frequency : np.array
        Numpy array containing frequency for all possible k-mers.
    """
    dictionary = {}
    for kmer in kmers:
        dictionary[kmer] = 0
    for i in range(len(sequence) - (len(kmers[0]) - 1)):
        key = sequence[i : i + len(kmers[0])]
        if key in dictionary:
            dictionary[key] = dictionary[key] + 1
    frequency = []
    for kmer in kmers:
        frequency.append(dictionary[kmer])
    return np.array(frequency)


def grouper(maximum_elements: int, items: list) -> np.array:
    """
    Return groups with a maximum of n elements for a given list.

    Parameters
    ----------
    maximum_elements : int
        Maximum number of elements per group.
    items : list
        List containing items to divide in groups.

    Returns
    -------
    groups : np.array
        Numpy array containing groups of items.
    """
    groups = []
    subgroup = []
    for item in items:
        if len(subgroup) < maximum_elements:
            subgroup.append(item)
        else:
            groups.append(subgroup)
            subgroup = [item]
    if len(subgroup) > 0:
        groups.append(subgroup)
    return np.array(groups, dtype=object)


def compute_group_frequency(sequences_and_kmers: tuple) -> np.array:
    """
    Compute k-mer frequency for a group of sequences.

    Parameters
    ----------
    sequences_and_kmers : tuple
        Tuple containing a list of sequences and k-mers.

    Returns
    -------
    frequencies : np.array
        Numpy array containing frequencies for a group of sequences.
    """
    frequencies = []
    sequences, kmers = sequences_and_kmers
    for sequence in sequences:
        frequencies.append(compute_kmer_frequency(sequence, kmers))
    return np.array(frequencies)


def compute_frequencies(
    sequences: list, kmers: list, threads: int = cpu_count(), batch_size: int = 100
) -> np.array:
    """
    Compute k-mer frequency for all sequences.

    Parameters
    ----------
    sequences : list
        List containing all sequences.
    kmers : list
        List containing all possible k-mers.
    threads : int, default='all CPUs'
        Number of threads to compute in parallel.
    batch_size : int, default=100
        Size of each batch to run in parallel.

    Returns
    -------
    frequencies : np.array
        Numpy array containing frequencies for all sequences.
    """
    logger.info("Computing k-mer frequency")
    sequences = [s.decode("utf-8") for s in sequences]
    executor = concurrent.futures.ProcessPoolExecutor(threads)
    futures = [
        executor.submit(compute_group_frequency, (group, kmers))
        for group in grouper(batch_size, sequences)
    ]
    concurrent.futures.wait(futures)
    frequencies = [f.result() for f in futures]
    frequencies = list(itertools.chain(*frequencies))
    return np.array(frequencies)


def extract_qiime2_ranks(taxonomy: str) -> np.array:
    """
    Split taxonomy by ranks.

    Parameters
    ----------
    taxonomy : str
        String with concatenated taxonomy.

    Returns
    -------
    ranks : np.array
        Numpy array where each item is a taxonomic rank.
    """
    ranks = taxonomy.split(";")
    return np.array(ranks)


def extract_qiime2_taxonomy(taxonomy: list) -> np.array:
    """
    Extract taxonomy from a list of strings.

    Parameters
    ----------
    taxonomy : list
        List String with concatenated taxonomy.

    Returns
    -------
    extracted_taxonomy : np.array
        Numpy array where each item is another array with taxonomic ranks.
    """
    extracted_taxonomy = []
    for record in taxonomy:
        extracted_taxonomy.append(extract_qiime2_ranks(record))
    return np.array(extracted_taxonomy)


def _extract_reads(reads) -> zip:
    """
    Extract IDs and sequences from DNAIterator.

    Parameters
    ----------
    reads : DNAIterator
        Iterator containing sequences.

    Returns
    -------
    _ : zip
        Zip object containing tuples with ID and sequence.
    """
    return zip(*[(r.metadata["id"], r._string) for r in reads])


def convert_taxonomy_to_qiime2(predictions: np.array) -> list:
    """
    Convert predictions made by HiTaC to QIIME2 taxonomy format.

    Parameters
    ----------
    predictions : np.array
        Predictions made by HiTaC.

    Returns
    -------
    taxonomy : list
        List containing converted taxonomy.
    """
    taxonomy = []
    for prediction in predictions:
        tax = ""
        for i in range(len(prediction) - 1):
            tax = tax + prediction[i] + ";"
        tax = tax + prediction[-1]
        taxonomy.append(tax)
    return taxonomy


# TODO: replace with binary search if speed becomes an issue
def search(key: str, items: list) -> int:
    """
    Search for a key index in a list.

    Parameters
    ----------
    key : str
        Key to search for.
    items : list
        List containing items to search.

    Returns
    -------
    index : int
        Index of the item in the list.
    """
    for i in range(len(items)):
        if key == items[i]:
            return i


def compute_confidence(
    classification: np.array,
    classes: np.array,
    predict_proba: np.array,
    threshold: float,
) -> tuple:
    """
    Compute confidence score for predictions and removes ranks if their confidence is lower than threshold.

    Parameters
    ----------
    classification : np.array
        Taxonomic predictions made by previous classifier.
    classes : np.array
        Classes in each taxonomic rank.
    predict_proba : np.array
        Prediction probability computed by the filter.
    threshold : float
        Minimum confidence score to keep taxonomic ranks

    Returns
    -------
    predictions, confidence : tuple
        Predictions with ranks above minimum threshold and confidence score for the lowest rank available.
    """
    predictions = []
    confidence = []
    for row in range(len(classification)):
        predictions.append([])
        confidence.append(-1)
        for rank in reversed(range(len(classification[row]))):
            if confidence[row] == -1:
                index = search(classification[row][rank], classes[rank])
                conf = predict_proba[rank][row][index]
                if conf >= threshold:
                    confidence[row] = conf
            if confidence[row] >= threshold:
                predictions[row].insert(0, classification[row][rank])
            else:
                predictions[row].insert(0, "")
    return predictions, confidence


def load_fasta(fasta_path: str, reference) -> tuple:
    """
    Load reference FASTA file.

    Parameters
    ----------
    fasta_path : str
        Path where the FASTA file is stored.
    reference : Bool
        Is this file the reference? True of False.

    Returns
    -------
    sequences, taxonomy : tuple
        Sequences and taxonomy loaded from FASTA file.
    """
    logger.info(f"Loading FASTA file {fasta_path}")
    with open(fasta_path) as fin:
        header = None
        sequence = None
        sequences = []
        headers = []
        for line in fin:
            if line.startswith(">"):
                if header:
                    sequences.append(str.encode(sequence))
                else:
                    header = line.strip()
                sequence = ""
                if reference:
                    headers.append(extract_taxxi_taxonomy(line.strip()))
                else:
                    headers.append(line.strip()[1:])
            else:
                sequence = sequence + line.strip()
        sequences.append(str.encode(sequence))
    if reference:
        return tuple(sequences), np.array(headers, dtype="object")
    else:
        return tuple(sequences), headers


def extract_taxxi_taxonomy(taxxi: str) -> str:
    """
    Convert taxonomy from TAXXI format to a format used by HiTaC.

    Parameters
    ----------
    taxxi : str
        Taxonomy in TAXXI format.

    Returns
    -------
    taxonomy : str
        Taxonomy in format used by HiTaC.
    """
    taxonomy = []
    for rank in taxxi.split(","):
        taxonomy.append(rank)
    taxonomy[0] = taxonomy[0][taxonomy[0].find("=") + 1 :]
    taxonomy[-1] = taxonomy[-1][:-1]
    return taxonomy


def convert_taxonomy_to_taxxi(predictions: np.array) -> list:
    """
    Convert predictions made by HiTaC to TAXXI taxonomy format.

    Parameters
    ----------
    predictions : np.array
        Predictions made by HiTaC.

    Returns
    -------
    taxonomy : list
        List containing converted taxonomy.
    """
    taxonomy = []
    for prediction in predictions:
        tax = ""
        for i in range(len(prediction) - 1):
            tax = tax + prediction[i] + ","
        tax = tax + prediction[-1]
        taxonomy.append(tax)
    return taxonomy


def save_tsv(output: TextIO, ids: List[str], taxonomy: List[str]) -> None:
    """
    Store TSV containing predictions.

    Parameters
    ----------
    output : TextIO
        The output stream to write to.
    ids : List[str]
        The IDs for the query sequences.
    taxonomy : List[str]
        The predicted taxonomy.
    """
    for id, tax in zip(ids, taxonomy):
        output.write(id)
        output.write("\t")
        output.write(tax)
        output.write("\n")


def get_logistic_regression() -> LogisticRegression:
    """
    Build a logistic regression classifier.

    Returns
    -------
    logistic_regression : LogisticRegression
        The logistic regression classifier
    """
    logistic_regression = LogisticRegression(
        solver="liblinear",
        multi_class="auto",
        class_weight="balanced",
        max_iter=10000,
        verbose=0,
        n_jobs=1,
    )
    return logistic_regression


def get_hierarchical_classifier(
    threads: int, tmp_dir: str = None
) -> LocalClassifierPerParentNode:
    """
    Build the hierarchical classifier.

    Parameters
    ----------
    threads : int
        The number of threads for training in parallel.
    tmp_dir : str
        Temporary directory to persist local classifiers that are trained. If the job needs to be restarted,
         it will skip the pre-trained local classifier found in the temporary directory.

    Returns
    -------
    hierarchical_classifier : LocalClassifierPerParentNode
        The hierarchical classifier.
    """
    logistic_regression = get_logistic_regression()
    hierarchical_classifier = LocalClassifierPerParentNode(
        local_classifier=logistic_regression, n_jobs=threads, verbose=5, tmp_dir=tmp_dir
    )
    return hierarchical_classifier


def get_hierarchical_filter(threads: int, tmp_dir: str = None) -> Filter:
    """
    Build the hierarchical filter.

    Parameters
    ----------
    threads : int
        The number of threads for training in parallel.
    tmp_dir : str
        Temporary directory to persist local classifiers that are trained. If the job needs to be restarted,
         it will skip the pre-trained local classifier found in the temporary directory.

    Returns
    -------
    hierarchical_filter : Filter
        The hierarchical filter.
    """
    logistic_regression = get_logistic_regression()
    hierarchical_filter = Filter(
        local_classifier=logistic_regression, n_jobs=threads, verbose=5, tmp_dir=tmp_dir
    )
    return hierarchical_filter


def load_classification(classification_path: str) -> np.ndarray:
    """
    Load a classification TSV file and extract taxonomy.

    Parameters
    ----------
    classification_path : str
        The path to the TSV file containing the predictions.

    Returns
    -------
    classification : np.ndarray
        The classification matrix.
    """
    classification = []
    with open(classification_path, "r") as fin:
        for line in fin:
            taxonomy = line.strip().split("\t")[-1].split(",")
            classification.append(taxonomy)
        return np.array(classification, dtype="object")
