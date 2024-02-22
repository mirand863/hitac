import argparse
import pandas as pd
import sys
import warnings
from argparse import Namespace
from glob import glob
from os.path import exists
from typing import List


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
        description="Create TAXXI metric table for a given dataset"
    )
    parser.add_argument(
        "--taxxi-metrics",
        type=str,
        required=True,
        help="Folder where metrics results are stored [default: results/taxxi_metrics]",
    )
    parser.add_argument(
        "--dataset",
        type=str,
        required=True,
        help="Dataset to compute metrics",
    )
    parser.add_argument(
        "--rank",
        type=str,
        required=True,
        help="Taxonomic rank to compute metrics",
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
    dataset: str,
    rank: str,
) -> List[str]:
    """
    Return all methods names.

    Parameters
    ----------
    taxxi_folder : str
        Path to the metrics folder.
    dataset : str
        Dataset to extract metrics from.
    rank : str
        Taxonomic rank to extract metrics from.

    Returns
    -------
    methods : List[str]
        Methods in metrics folder.
    """
    paths = glob(f"{taxxi_folder}/*/{dataset}/{rank}.tsv", recursive=True)
    methods = [path.split("/")[2] for path in paths]
    methods = list(set(methods))
    methods.remove("hitac_filter_qiime")
    methods.remove("hitac_qiime")
    methods.sort()
    return methods


pretty_datasets = {
    "sp_rdp_its.90": "SP RDP ITS 90",
    "sp_rdp_its.95": "SP RDP ITS 95",
    "sp_rdp_its.97": "SP RDP ITS 97",
    "sp_rdp_its.99": "SP RDP ITS 99",
    "sp_rdp_its.100": "SP RDP ITS 100",
}
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
pretty_ranks = {
    "p": "phylum",
    "c": "class",
    "o": "order",
    "f": "family",
    "g": "genus",
    "s": "species",
}


def get_value(line):
    value = line.strip().split("\t")[-1]
    if value == ".":
        return float("nan")
    else:
        return float(value)


def main():  # pragma: no cover
    """Generate TAXXI metric table."""
    args = parse_args(sys.argv[1:])
    with open(args.output, "w") as output:
        methods = get_methods(args.taxxi_metrics, args.dataset, args.rank)
        results = {
            "method": [],
            "acc": [],
            "mcr": [],
            "ocr": [],
            "tpr": [],
            "ucr": [],
        }
        for method in methods:
            file = f"{args.taxxi_metrics}/{method}/{args.dataset}/{args.rank}.tsv"
            if exists(file):
                with open(file, "r") as fin:
                    results["tpr"].append(get_value(fin.readline()))
                    results["ucr"].append(get_value(fin.readline()))
                    results["mcr"].append(get_value(fin.readline()))
                    results["ocr"].append(get_value(fin.readline()))
                    results["acc"].append(get_value(fin.readline()))
                    results["method"].append(pretty_name[method])
        results_df = pd.DataFrame(data=results)
        # Sort values by accuracy
        results_df.sort_values(
            by=["acc"],
            inplace=True,
            ascending=[False],
        )
        # Write results
        output.write(
            results_df.to_latex(
                index=False,
                bold_rows=True,
                label=f"taxxi:{args.dataset}:{pretty_ranks[args.rank]}",
                caption=f"TAXXI metrics computed for the dataset {pretty_datasets[args.dataset]} at the {pretty_ranks[args.rank]} level.",
            )
        )


if __name__ == "__main__":  # pragma: no cover
    main()
