#!/usr/bin/env python3
"""Script to fit hierarchical classifier."""
import sys

import argparse
import pickle
from argparse import Namespace
from hitac._utils import (
    load_fasta,
    compute_frequencies,
    compute_possible_kmers,
    get_hierarchical_classifier,
)
from multiprocessing import cpu_count
from sklearn.model_selection import train_test_split


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
        description="Fit hierarchical classifier",
    )
    parser.add_argument(
        "--reference",
        type=str,
        required=True,
        help="Input FASTA file with reference sequence(s) to train model",
    )
    parser.add_argument(
        "--kmer",
        type=int,
        required=False,
        default=6,
        help="K-mer size for feature extraction [default: 6]",
    )
    parser.add_argument(
        "--threads",
        type=int,
        required=False,
        default=cpu_count(),
        help="Number of threads to train in parallel [default: all]",
    )
    parser.add_argument(
        "--calibration-method",
        type=str,
        required=False,
        default=None,
        help="Calibration method to compute prediction probability",
    )
    parser.add_argument(
        "--calibration-percentage",
        type=float,
        required=False,
        default=None,
        help="Percentage of training sequences allocated for calibration",
    )
    parser.add_argument(
        "--classifier",
        type=str,
        required=True,
        help="Path to store trained hierarchical classifier",
    )
    return parser.parse_args(args)


def main():  # pragma: no cover
    """Fit HiTaC."""
    args = parse_args(sys.argv[1:])
    kmers = compute_possible_kmers(args.kmer)
    training_sequences, hierarchy = load_fasta(fasta_path=args.reference, reference=True)
    frequencies = compute_frequencies(training_sequences, kmers, args.threads)
    x_train, x_cal, y_train, y_cal = train_test_split(
        frequencies, hierarchy, test_size=args.calibration_percentage, random_state=42
    )
    hierarchical_classifier = get_hierarchical_classifier(
        threads=args.threads,
        calibration_method=args.calibration_method,
    )
    hierarchical_classifier.fit(x_train, y_train)
    hierarchical_classifier.calibrate(x_cal, y_cal)
    pickle.dump(hierarchical_classifier, open(args.classifier, "wb"))


if __name__ == "__main__":  # pragma: no cover
    main()
