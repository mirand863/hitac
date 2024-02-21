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
    parser = argparse.ArgumentParser(description="Create ML tables for given dataset")
    parser.add_argument(
        "--ml-metrics",
        type=str,
        required=False,
        default="results/ml_metrics",
        help="Folder where metrics results are stored [default: results/ml_metrics]",
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
        default="results/figures_and_tables/ml_metrics/sp_rdp_its_100.txt",
        help="Output to write results [default: results/figures_and_tables/ml_metrics/sp_rdp_its_100.txt]",
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
    accuracy = round(float(df["accuracy"].iloc[0]) * 100, 2)
    balanced_accuracy = round(float(df["balanced_accuracy"].iloc[0]) * 100, 2)
    f1_micro = round(float(df["f1_micro"].iloc[0]) * 100, 2)
    f1_macro = round(float(df["f1_macro"].iloc[0]) * 100, 2)
    f1_weighted = round(float(df["f1_weighted"].iloc[0]) * 100, 2)
    precision_micro = round(float(df["precision_micro"].iloc[0]) * 100, 2)
    precision_macro = round(float(df["precision_macro"].iloc[0]) * 100, 2)
    precision_weighted = round(float(df["precision_weighted"].iloc[0]) * 100, 2)
    recall_micro = round(float(df["recall_micro"].iloc[0]) * 100, 2)
    recall_macro = round(float(df["recall_macro"].iloc[0]) * 100, 2)
    recall_weighted = round(float(df["recall_weighted"].iloc[0]) * 100, 2)
    jaccard_micro = round(float(df["jaccard_micro"].iloc[0]) * 100, 2)
    jaccard_macro = round(float(df["jaccard_macro"].iloc[0]) * 100, 2)
    jaccard_weighted = round(float(df["jaccard_weighted"].iloc[0]) * 100, 2)
    results["accuracy"].append(accuracy)
    results["balanced_accuracy"].append(balanced_accuracy)
    results["f1_micro"].append(f1_micro)
    results["f1_macro"].append(f1_macro)
    results["f1_weighted"].append(f1_weighted)
    results["precision_micro"].append(precision_micro)
    results["precision_macro"].append(precision_macro)
    results["precision_weighted"].append(precision_weighted)
    results["recall_micro"].append(recall_micro)
    results["recall_macro"].append(recall_macro)
    results["recall_weighted"].append(recall_weighted)
    results["jaccard_micro"].append(jaccard_micro)
    results["jaccard_macro"].append(jaccard_macro)
    results["jaccard_weighted"].append(jaccard_weighted)


def main():  # pragma: no cover
    """Generate ML tables."""
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
