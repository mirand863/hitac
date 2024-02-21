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
        description="Create TAXXI tables for given dataset"
    )
    parser.add_argument(
        "--taxxi-metrics",
        type=str,
        required=False,
        default="results/taxxi_metrics",
        help="Folder where metrics results are stored [default: results/taxxi_metrics]",
    )
    parser.add_argument(
        "--dataset",
        type=str,
        required=False,
        default="sp_rdp_its.90",
        help="Dataset to compute metrics [default: sp_rdp_its.90]",
    )
    parser.add_argument(
        "--rank",
        type=str,
        required=False,
        default="g",
        help="Taxonomic rank to compute metrics [default: g]",
    )
    parser.add_argument(
        "--output",
        type=str,
        required=False,
        default="results/figures_and_tables/taxxi_metrics/sp_rdp_its_100.txt",
        help="Output to write results [default: results/figures_and_tables/taxxi_metrics/sp_rdp_its_100.txt]",
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
    "hitac_qiime": "HiTaC\_QIIME",
    "hitac_standalone": "HiTaC\_standalone",
    "q2sk": r"Q2\_SK",
    "nbc50": "NBC50",
    "nbc80": "NBC80",
    "rdp50": "RDP50",
    "rdp80": "RDP80",
    "ct2": "CT2",
    "metaxa2": "Metaxa2",
    "ktop": "KTOP",
    "top": "TOP",
    "hitac_filter_qiime": r"HiTaC\_Filter\_QIIME",
    "hitac_filter_standalone": r"HiTaC\_Filter\_standalone",
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
    """Generate TAXXI tables."""
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
                    tpr = get_value(fin.readline())
                    ucr = get_value(fin.readline())
                    mcr = get_value(fin.readline())
                    ocr = get_value(fin.readline())
                    acc = get_value(fin.readline())
                    results["tpr"].append(tpr)
                    results["ucr"].append(ucr)
                    results["mcr"].append(mcr)
                    results["ocr"].append(ocr)
                    results["acc"].append(acc)
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
