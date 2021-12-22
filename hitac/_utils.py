"""Helper functions for data manipulation."""
import concurrent.futures
import itertools
from itertools import product
from multiprocessing import cpu_count

import numpy as np


def compute_possible_kmers(kmer_size: int = 6, alphabet: str = "ACGT") -> np.array:
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
    kmers : np.array
        Numpy array containing all possible k-mers.
    """
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
    Convert predictions made by HiClass to QIIME2 taxonomy format.

    Parameters
    ----------
    predictions : np.array
        Predictions made by HiClass.

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
                predictions[row].insert(0, '')
    return predictions, confidence
