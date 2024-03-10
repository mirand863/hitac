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
        description="Create hierarchical metric table for a given dataset"
    )
    parser.add_argument(
        "--hierarchical-metrics",
        type=str,
        required=True,
        help="Folder where metrics results are stored",
    )
    parser.add_argument(
        "--dataset",
        type=str,
        required=True,
        help="Dataset to compute metrics",
    )
    parser.add_argument(
        "--output",
        type=str,
        required=True,
        help="Output to write results",
    )
    return parser.parse_args(args)


def get_methods(
    hierarchical_folder: str,
    dataset: str,
) -> List[str]:
    """
    Return all methods names.

    Parameters
    ----------
    hierarchical_folder : str
        Path to the metrics folder.
    dataset : str
        Dataset to extract metrics from.

    Returns
    -------
    methods : List[str]
        Methods in metrics folder.
    """
    paths = glob(f"{hierarchical_folder}/*/{dataset}.tsv", recursive=True)
    methods = [path.split("/")[2] for path in paths]
    methods = list(set(methods))
    methods.remove("hitac_filter_qiime")
    methods.remove("hitac_qiime")
    methods.sort()
    return methods


pretty_name = {
    "q2vs": r"Q2\_VS",
    "sintax50": "SINTAX50",
    "sintax80": "SINTAX80",
    "btop": "BTOP",
    "microclass": "Microclass",
    "spingo": "SPINGO",
    "knn": "KNN",
    "q1": "Q1",
    "hitac_standalone": "HiTaC",
    "q2sk": r"Q2\_SK",
    "nbc50": "NBC50",
    "nbc80": "NBC80",
    "rdp50": "RDP50",
    "rdp80": "RDP80",
    "ct2": "CT2",
    "metaxa2": "Metaxa2",
    "ktop": "KTOP",
    "top": "TOP",
    "hitac_filter_standalone": r"HiTaC\_Filter",
    "q2blast": r"Q2\_BLAST",
    "blca": "BLCA",
    "ct1": "CT1",
}


def main():  # pragma: no cover
    """Generate hierarchical metric table."""
    args = parse_args(sys.argv[1:])
    with open(args.output, "w") as output:
        methods = get_methods(args.hierarchical_metrics, args.dataset)
        results = {
            "method": [],
            "fscore": [],
            "precision": [],
            "recall": [],
        }
        for method in methods:
            file = f"results/hierarchical_metrics/{method}/{args.dataset}.tsv"
            if exists(file):
                df = pd.read_csv(file, sep="\t")
                results["method"].append(pretty_name[method])
                results["fscore"].append(round(float(df["f1"].iloc[0]) * 100, 2))
                results["precision"].append(
                    round(float(df["precision"].iloc[0]) * 100, 2)
                )
                results["recall"].append(round(float(df["recall"].iloc[0]) * 100, 2))
        results_df = pd.DataFrame(data=results)
        # Sort values by f1-score
        results_df.sort_values(
            by=["fscore", "method"],
            inplace=True,
            ascending=[False, False],
        )
        results_df.to_csv(args.output, index=False, float_format="%.2f")


if __name__ == "__main__":  # pragma: no cover
    main()
