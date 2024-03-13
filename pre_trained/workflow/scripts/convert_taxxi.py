import argparse
import sys
from argparse import Namespace

import screed


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
    parser = argparse.ArgumentParser(description="Convert QIIME2 input to TAXXI format")
    parser.add_argument(
        "--fasta",
        type=str,
        required=True,
        help="Path to input FASTA file.",
    )
    parser.add_argument(
        "--taxonomy",
        type=str,
        required=True,
        help="Path to input taxonomy file.",
    )
    parser.add_argument(
        "--output",
        type=str,
        required=True,
        help="Output to write results",
    )
    return parser.parse_args(args)


def main():  # pragma: no cover
    """Convert QIIME2 to TAXXI."""
    args = parse_args(sys.argv[1:])
    with open(args.output, "w") as output:
        with screed.open(args.fasta) as seqfile:
            with open(args.taxonomy) as taxfile:
                taxfile.readline()  # skip header
                for read in seqfile:
                    taxonomy = taxfile.readline().split("\t")[-1].strip()
                    taxonomy = taxonomy.replace(";", ",") + ";"
                    output.write(f">{read.name};tax={taxonomy}\n")
                    output.write(f"{read.sequence}\n")


if __name__ == "__main__":  # pragma: no cover
    main()
