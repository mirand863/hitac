#!/usr/bin/env python3
"""Script to fit hierarchical classifier."""
import argparse
import pickle
import sys
from argparse import Namespace
from multiprocessing import cpu_count

from hitac._utils import (
    load_fasta,
    compute_frequencies,
    compute_possible_kmers,
    get_hierarchical_classifier,
)


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
    training_sequences, y_train = load_fasta(fasta_path=args.reference, reference=True)
    x_train = compute_frequencies(training_sequences, kmers, args.threads)
    hierarchical_classifier = get_hierarchical_classifier(args.threads)
    hierarchical_classifier.fit(x_train, y_train)
    pickle.dump(hierarchical_classifier, open(args.classifier, "wb"))


if __name__ == "__main__":  # pragma: no cover
    main()
