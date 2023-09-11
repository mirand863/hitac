#!/usr/bin/env python3
"""Script to classify sequences with hierarchical classifier."""
import argparse
import pickle
import sys
from argparse import Namespace
from multiprocessing import cpu_count

from hitac._utils import (
    compute_possible_kmers,
    load_fasta,
    compute_frequencies,
    convert_taxonomy_to_taxxi,
    save_tsv,
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
        description="Predict with hierarchical classifier",
    )
    parser.add_argument(
        "--reads",
        type=str,
        required=True,
        help="Input FASTA file with sequence(s) to classify",
    )
    parser.add_argument(
        "--classifier",
        type=str,
        required=True,
        help="Path to trained hierarchical classifier",
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
        "--classification",
        type=str,
        required=True,
        help="Path to store predictions",
    )
    return parser.parse_args(args)


def main():  # pragma: no cover
    """Classify sequences using HiTaC."""
    args = parse_args(sys.argv[1:])
    kmers = compute_possible_kmers(args.kmer)
    test_sequences, seq_ids = load_fasta(fasta_path=args.reads, reference=False)
    x_test = compute_frequencies(test_sequences, kmers, args.threads)
    classifier = pickle.load(open(args.classifier, "rb"))
    predictions = classifier.predict(x_test)
    taxonomy = convert_taxonomy_to_taxxi(predictions)
    with open(args.classification, "w") as output:
        save_tsv(output, seq_ids, taxonomy)


if __name__ == "__main__":  # pragma: no cover
    main()
