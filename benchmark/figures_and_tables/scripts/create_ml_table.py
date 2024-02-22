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
    "q2vs": r"Q2_VS",
    "sintax50": "SINTAX50",
    "sintax80": "SINTAX80",
    "btop": "BTOP",
    "microclass": "Microclass",
    "spingo": "SPINGO",
    "knn": "KNN",
    "q1": "Q1",
    "hitac_standalone": "HiTaC",
    "q2sk": r"Q2_SK",
    "nbc50": "NBC50",
    "nbc80": "NBC80",
    "rdp50": "RDP50",
    "rdp80": "RDP80",
    "ct2": "CT2",
    "metaxa2": "Metaxa2",
    "ktop": "KTOP",
    "top": "TOP",
    "hitac_filter_standalone": r"HiTaC_Filter",
    "q2blast": r"Q2_BLAST",
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
        "Method": [],
        "Accuracy": [],
        "Balanced Accuracy": [],
        "F1-score Micro": [],
        "F1-score Macro": [],
        "F1-score Weighted": [],
        "Precision Micro": [],
        "Precision Macro": [],
        "Precision Weighted": [],
        "Recall Micro": [],
        "Recall Macro": [],
        "Recall Weighted": [],
        "Jaccard Micro": [],
        "Jaccard Macro": [],
        "Jaccard Weighted": [],
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
    results["Accuracy"].append(round(float(df["accuracy"].iloc[0]) * 100, 2))
    results["Balanced Accuracy"].append(
        round(float(df["balanced_accuracy"].iloc[0]) * 100, 2)
    )
    results["F1-score Micro"].append(round(float(df["f1_micro"].iloc[0]) * 100, 2))
    results["F1-score Macro"].append(round(float(df["f1_macro"].iloc[0]) * 100, 2))
    results["F1-score Weighted"].append(
        round(float(df["f1_weighted"].iloc[0]) * 100, 2)
    )
    results["Precision Micro"].append(
        round(float(df["precision_micro"].iloc[0]) * 100, 2)
    )
    results["Precision Macro"].append(
        round(float(df["precision_macro"].iloc[0]) * 100, 2)
    )
    results["Precision Weighted"].append(
        round(float(df["precision_weighted"].iloc[0]) * 100, 2)
    )
    results["Recall Micro"].append(round(float(df["recall_micro"].iloc[0]) * 100, 2))
    results["Recall Macro"].append(round(float(df["recall_macro"].iloc[0]) * 100, 2))
    results["Recall Weighted"].append(
        round(float(df["recall_weighted"].iloc[0]) * 100, 2)
    )
    results["Jaccard Micro"].append(round(float(df["jaccard_micro"].iloc[0]) * 100, 2))
    results["Jaccard Macro"].append(round(float(df["jaccard_macro"].iloc[0]) * 100, 2))
    results["Jaccard Weighted"].append(
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
                results["Method"].append(pretty_name[method])
                load_and_append(file, results)
        results_df = pd.DataFrame(data=results)
        # Sort values by accuracy
        results_df.sort_values(
            by=["Accuracy"],
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
