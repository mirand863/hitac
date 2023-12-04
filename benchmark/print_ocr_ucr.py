#!/usr/bin/env python3
"""Script to get the over-classification and under-classification results."""
import argparse
import sys
from argparse import Namespace
from collections import OrderedDict
from glob import glob
from typing import TextIO


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
        description="Get over-classification and under-classification results for a given dataset and taxonomic rank"
    )
    parser.add_argument(
        "--metrics",
        type=str,
        required=False,
        default="results/taxxi_metrics",
        help="Folder where metrics are stored [default: results/taxxi_metrics]",
    )
    parser.add_argument(
        "--dataset",
        type=str,
        required=False,
        default="sp_rdp_its.90",
        help="Dataset to get results [default: sp_rdp_its.90]",
    )
    parser.add_argument(
        "--rank",
        type=str,
        required=False,
        default="g",
        help="Taxonomic rank to get results [default: g]",
    )
    parser.add_argument(
        "--output",
        type=str,
        required=False,
        default="results/images/ocr_ucr_90_g.csv",
        help="Output to write results [default: results/images/ocr_ucr_90_g.csv]",
    )
    return parser.parse_args(args)


def get_methods(metrics_folder: str) -> dict:
    """
    Return all methods with OCR and UCR set to NaN.

    Parameters
    ----------
    metrics_folder : str
        Path to the metrics folder.

    Returns
    -------
    methods : dict
        Methods in metrics folder.
    """
    methods_paths = glob(f"{metrics_folder}/*", recursive=True)
    methods = {
        method.split("/")[-1]: {"OCR": "NaN", "UCR": "NaN"} for method in methods_paths
    }
    return methods


def compute_scores(metrics_folder: str, dataset: str, rank: str, methods: dict) -> None:
    """
    Compute OCR and UCR for a given dataset and taxonomic rank.

    Parameters
    ----------
    metrics_folder : str
        Path to the metrics folder.
    dataset : str
        Dataset to compute metrics, e.g., sp_rdp_its.90.
    rank : str
        Taxonomic rank to compute metrics, e.g., g, s, c, etc.
    methods : dict
        Methods to compute metrics.
    """
    for method in methods:
        file = metrics_folder + "/" + method + "/" + dataset + "/" + rank + ".tsv"
        with open(file, "r") as fin:
            ocr = ucr = "."
            for line in fin:
                if line.split("\t")[3] == "OCR":
                    ocr = line.split("\t")[-1].strip()
                elif line.split("\t")[3] == "UCR":
                    ucr = line.split("\t")[-1].strip()
            if ocr != "." and ucr != ".":
                methods[method]["OCR"] = float(ocr)
                methods[method]["UCR"] = float(ucr)


def sort(methods: dict) -> OrderedDict:
    """
    Sort methods in alphabetical order.

    Parameters
    ----------
    methods : dict
        All methods in the benchmark.

    Returns
    -------
    sorted_methods : OrderedDict
        Sorted methods in alphabetical order.
    """
    sorted_methods = OrderedDict(sorted(methods.items()))
    return sorted_methods


def get_ocr_ucr(metrics_folder, dataset, rank):
    """
    Compute OCR and UCR for all methods.

    Parameters
    ----------
    metrics_folder : str
        Path to the metrics folder.
    dataset : str
        Dataset to compute metrics.
    rank : str
        Taxonomic rank.

    Returns
    -------
    ocr_ucr : dict
        Methods in metrics folder with OCR and UCR scores.
    """
    methods = get_methods(metrics_folder)
    compute_scores(metrics_folder, dataset, rank, methods)
    ocr_ucr = sort(methods)
    return ocr_ucr


def write_csv(scores: dict, output: TextIO) -> None:
    """
    Write output file in CSV format.

    Parameters
    ----------
    scores : dict
        Scores computed for all methods.
    output : TextIO
        Path to write output file in CSV format.
    """
    pretty_names = {
        "q2vs": "Q2_VS",
        "sintax50": "SINTAX50",
        "sintax80": "SINTAX80",
        "btop": "BTOP",
        "microclass": "Microclass",
        "spingo": "SPINGO",
        "knn": "KNN",
        "q1": "Q1",
        "hitac_standalone": "HiTaC",
        "q2sk": "Q2_SK",
        "nbc80": "NBC80",
        "rdp50": "RDP50",
        "ct2": "CT2",
        "metaxa2": "Metaxa2",
        "ktop": "KTOP",
        "top": "TOP",
        "hitac_filter_standalone": "HiTaC_Filter",
        "nbc50": "NBC50",
        "rdp80": "RDP80",
        "q2blast": "Q2_BLAST",
        "blca": "BLCA",
        "ct1": "CT1",
    }
    output.write("Method,OCR,UCR\n")
    for method in scores:
        if (
            method in pretty_names
            and scores[method]["OCR"] != "NaN"
            and scores[method]["UCR"] != "NaN"
        ):
            output.write(
                f"{pretty_names[method]},{scores[method]['OCR']},{scores[method]['UCR']}\n"
            )


def main():  # pragma: no cover
    """Get over-classification and under-classification results."""
    args = parse_args(sys.argv[1:])
    ocr_ucr = get_ocr_ucr(args.metrics, args.dataset, args.rank)
    with open(args.output, "w") as csv:
        write_csv(ocr_ucr, csv)


if __name__ == "__main__":
    main()  # pragma: no cover
