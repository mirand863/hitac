"""Helper functions for data manipulation."""
import logging
import os

import numpy as np
import pandas as pd

logger = logging.getLogger()


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


def load_features(features_dir: str) -> np.array:
    """
    Load pre-computed features from a folder.

    Parameters
    ----------
    features_dir : str
        Folder containing extracted features.

    Returns
    -------
    features : np.array
        Numpy array with extracted features.
    """
    os.chdir(features_dir)
    X_train = pd.read_csv("ftrain.csv").to_numpy()
    Y_train = []
    with open("DNC.csv") as fin:
        fin.readline()  # skip header
        line = fin.readline()
        while line:
            line = line.strip().split(",")
            domain = line[0][line[0].find("=") + 1 :].replace(":", "__")
            phylum = line[1].replace(":", "__")
            class_ = line[2].replace(":", "__")
            order = line[3].replace(":", "__")
            family = line[4].replace(":", "__")
            genus = line[5].replace(":", "__")
            species = line[6].replace(":", "__")[:-1]
            Y_train.append([domain, phylum, class_, order, family, genus, species])
            line = fin.readline()
        Y_train = np.array(Y_train)
        return X_train, Y_train


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
                predictions[row].insert(0, "")
    return predictions, confidence
