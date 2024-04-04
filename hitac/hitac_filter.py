#!/usr/bin/env python3
"""Script to classify sequences with hierarchical classifier."""
import sys

import argparse
import numpy as np
import pickle
from argparse import Namespace
from hitac._utils import convert_taxonomy_to_taxxi, load_fasta, save_tsv


def parse_args(args: list) -> Namespace:
    """
    Parse a list of arguments.

    Parameters
    ----------
    args : list
        Arguments to parse.

    Returns
    -------
    _ : Namespace
        Parsed arguments.
    """
    parser = argparse.ArgumentParser(
        description="Predict with hierarchical classifier",
    )
    parser.add_argument(
        "--classifier",
        type=str,
        required=True,
        help="Path to trained hierarchical classifier",
    )
    parser.add_argument(
        "--probabilities",
        type=str,
        required=True,
        help="Path to stored probabilities",
    )
    parser.add_argument(
        "--classification",
        type=str,
        required=True,
        help="Path to stored predictions",
    )
    parser.add_argument(
        "--filtered-sequences",
        type=str,
        required=True,
        help="Path to stored filtered predictions",
    )
    parser.add_argument(
        "--threshold",
        type=float,
        required=True,
        help="Threshold to filter sequences",
    )
    parser.add_argument(
        "--reads",
        type=str,
        required=True,
        help="Input FASTA file with sequence(s) to classify",
    )
    return parser.parse_args(args)


def main():  # pragma: no cover
    """Compute the probabilities of sequences using HiTaC."""
    args = parse_args(sys.argv[1:])
    all_predictions = pickle.load(open(args.classification, "rb"))
    classifier = pickle.load(open(args.classifier, "rb"))
    all_probabilities = pickle.load(open(args.probabilities, "rb"))
    for level in range(len(all_probabilities) - 1, -1, -1):
        predictions = all_predictions[:,level]
        probabilities = all_probabilities[level]
        classes = classifier.classes_[level]
        classes_columns = {k:v for (v, k) in enumerate(classes)}
        filtered_predictions = []
        for prob, pred in zip(probabilities, predictions):
            if prob[classes_columns[pred]] >= args.threshold:
                filtered_predictions.append(pred)
            else:
                filtered_predictions.append("")
        all_predictions[:, level] = filtered_predictions
    taxonomy = convert_taxonomy_to_taxxi(all_predictions)
    test_sequences, seq_ids = load_fasta(fasta_path=args.reads, reference=False)
    with open(args.filtered_sequences, "w") as output:
        save_tsv(output, seq_ids, taxonomy)


if __name__ == "__main__":  # pragma: no cover
    main()
