import argparse
import sys
from argparse import Namespace
from glob import glob
from os.path import exists
from typing import List

import pandas as pd


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
        description="Extract over-classification and under-classification rates"
    )
    parser.add_argument(
        "--taxxi-metrics",
        type=str,
        required=True,
        help="Folder where metrics results are stored",
    )
    parser.add_argument(
        "--dataset",
        type=str,
        required=True,
        help="Dataset to plot figure",
    )
    parser.add_argument(
        "--output",
        type=str,
        required=True,
        help="Output to write results",
    )
    return parser.parse_args(args)


def get_methods(
    taxxi_folder: str,
) -> List[str]:
    """
    Return all methods names.

    Parameters
    ----------
    taxxi_folder : str
        Path to the metrics folder.

    Returns
    -------
    methods : List[str]
        Methods in metrics folder.
    """
    paths = glob(f"{taxxi_folder}/*/*/*.tsv", recursive=True)
    methods = [path.split("/")[2] for path in paths]
    methods = list(set(methods))
    methods.remove("hitac_filter_qiime")
    methods.remove("hitac_qiime")
    methods.sort()
    return methods


ranks = {
    "sp_rdp_its.90": "g",
    "sp_rdp_its.95": "g",
    "sp_rdp_its.97": "g",
    "sp_rdp_its.99": "s",
    "sp_rdp_its.100": "s",
}

pretty_name = {
    "hitac_filter_standalone": "HiTaC_Filter",
    "hitac_standalone": "HiTaC",
    "q2vs": "Q2_VS",
    "ct2": "CT2",
    "nbc80": "NBC80",
    "rdp80": "RDP80",
    "sintax50": "SINTAX50",
    "sintax80": "SINTAX80",
    "q2blast": "Q2_BLAST",
    "metaxa2": "Metaxa2",
    "knn": "KNN",
    "nbc50": "NBC50",
    "q2sk": "Q2_SK",
    "rdp50": "RDP50",
    "ct1": "CT1",
    "btop": "BTOP",
    "microclass": "Microclass",
    "top": "TOP",
    "ktop": "KTOP",
    "blca": "BLCA",
    "q1": "Q1",
    "spingo": "SPINGO",
}

results = {
    "Method": [],
    "UCR": [],
    "OCR": [],
}


def main():  # pragma: no cover
    """Get accuracy from TAXXI metrics."""
    args = parse_args(sys.argv[1:])
    methods = get_methods(args.taxxi_metrics)
    for method in methods:
        file = f"{args.taxxi_metrics}/{method}/{args.dataset}/{ranks[args.dataset]}.tsv"
        if exists(file):
            with open(file, "r") as fin:
                fin.readline()
                line = fin.readline()
                ucr = float(line.split("\t")[-1].strip())
                fin.readline()
                line = fin.readline()
                try:
                    ocr = float(line.split("\t")[-1].strip())
                except ValueError:
                    ocr = float("nan")
                results["Method"].append(pretty_name[method])
                results["UCR"].append(ucr)
                results["OCR"].append(ocr)
    results_df = pd.DataFrame(data=results)
    results_df.to_csv(args.output, index=False, float_format="%.2f", na_rep="NaN")


if __name__ == "__main__":  # pragma: no cover
    main()
