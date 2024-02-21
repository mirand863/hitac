import argparse
import pandas as pd
import sys
import warnings
from argparse import Namespace
from glob import glob
from os.path import exists
from typing import List, Dict


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
        description="Create ML metric table for a given dataset"
    )
    parser.add_argument(
        "--ml-metrics",
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
    ml_folder: str,
    dataset: str,
    rank: str,
) -> List[str]:
    """
    Return all methods names.

    Parameters
    ----------
    ml_folder : str
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
    paths = glob(f"{ml_folder}/*/{dataset}/{rank}.tsv", recursive=True)
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


def initialize_results() -> Dict[str, List]:
    """
    Initialize the dictionary that stores the results.

    Returns
    -------
    results : Dict[str, List]
        Dictionary that stores the results
    """
    results = {
        "method": [],
        "accuracy": [],
        "balanced_accuracy": [],
        "f1_micro": [],
        "f1_macro": [],
        "f1_weighted": [],
        "precision_micro": [],
        "precision_macro": [],
        "precision_weighted": [],
        "recall_micro": [],
        "recall_macro": [],
        "recall_weighted": [],
        "jaccard_micro": [],
        "jaccard_macro": [],
        "jaccard_weighted": [],
    }
    return results


def load_and_append(file: str, results: Dict[str, List]) -> None:
    """
    Load the results and append them to the results dictionary.

    Parameters
    ----------
    file : str
        The path to the file to load.
    results : Dict[str, List]
        The dictionary that stores the results.
    """
    df = pd.read_csv(file, sep="\t")
    results["accuracy"].append(round(float(df["accuracy"].iloc[0]) * 100, 2))
    results["balanced_accuracy"].append(
        round(float(df["balanced_accuracy"].iloc[0]) * 100, 2)
    )
    results["f1_micro"].append(round(float(df["f1_micro"].iloc[0]) * 100, 2))
    results["f1_macro"].append(round(float(df["f1_macro"].iloc[0]) * 100, 2))
    results["f1_weighted"].append(round(float(df["f1_weighted"].iloc[0]) * 100, 2))
    results["precision_micro"].append(
        round(float(df["precision_micro"].iloc[0]) * 100, 2)
    )
    results["precision_macro"].append(
        round(float(df["precision_macro"].iloc[0]) * 100, 2)
    )
    results["precision_weighted"].append(
        round(float(df["precision_weighted"].iloc[0]) * 100, 2)
    )
    results["recall_micro"].append(round(float(df["recall_micro"].iloc[0]) * 100, 2))
    results["recall_macro"].append(round(float(df["recall_macro"].iloc[0]) * 100, 2))
    results["recall_weighted"].append(
        round(float(df["recall_weighted"].iloc[0]) * 100, 2)
    )
    results["jaccard_micro"].append(round(float(df["jaccard_micro"].iloc[0]) * 100, 2))
    results["jaccard_macro"].append(round(float(df["jaccard_macro"].iloc[0]) * 100, 2))
    results["jaccard_weighted"].append(
        round(float(df["jaccard_weighted"].iloc[0]) * 100, 2)
    )


def main():  # pragma: no cover
    """Generate ML metric table."""
    args = parse_args(sys.argv[1:])
    with open(args.output, "w") as output:
        methods = get_methods(args.ml_metrics, args.dataset, args.rank)
        results = initialize_results()
        for method in methods:
            file = f"{args.ml_metrics}/{method}/{args.dataset}/{args.rank}.tsv"
            if exists(file):
                results["method"].append(pretty_name[method])
                load_and_append(file, results)
        results_df = pd.DataFrame(data=results)
        # Sort values by accuracy
        results_df.sort_values(
            by=["accuracy"],
            inplace=True,
            ascending=[False],
        )
        # Save results
        output.write(
            results_df.to_latex(
                index=False,
                bold_rows=True,
                label=f"ml:{args.dataset}:{pretty_ranks[args.rank]}",
                caption=f"Machine learning metrics computed for the dataset {pretty_datasets[args.dataset]} at the {pretty_ranks[args.rank]} level.",
            )
        )


if __name__ == "__main__":  # pragma: no cover
    main()
