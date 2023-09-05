#!/usr/bin/env python3
"""Script to filter sequences with hierarchical filter."""
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
    load_classification,
    compute_confidence,
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
        description="Filter sequences with HiTaC",
    )
    parser.add_argument(
        "--filter",
        type=str,
        required=True,
        help="Path to trained hierarchical filter",
    )
    parser.add_argument(
        "--reads",
        type=str,
        required=True,
        help="Input FASTA file with sequence(s) to filter",
    )
    parser.add_argument(
        "--classification",
        type=str,
        required=True,
        help="Path to predictions made by HiTaC's classifier",
    )
    parser.add_argument(
        "--threshold",
        type=float,
        required=False,
        default=0.7,
        help="Confidence threshold for limiting taxonomic depth. Set to 0 to compute confidence score but not apply it to limit the taxonomic depth of the assignments. [default: 0.7]",
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
        "--filtered-classification",
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
    hierarchical_filter = pickle.load(open(args.filter, "rb"))
    predict_proba = hierarchical_filter.predict_proba(x_test)
    classes = hierarchical_filter.classes_
    classification = load_classification(args.classification)
    predictions, confidence = compute_confidence(
        classification, classes, predict_proba, args.threshold
    )
    taxonomy = [tax.rstrip(",") for tax in convert_taxonomy_to_taxxi(predictions)]
    with open(args.filtered_classification, "w") as output:
        save_tsv(output, seq_ids, taxonomy)


if __name__ == "__main__":  # pragma: no cover
    main()
