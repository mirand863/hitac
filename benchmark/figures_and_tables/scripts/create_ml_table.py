import argparse
import sys
from argparse import Namespace
from glob import glob
from os.path import exists
from typing import List, Dict

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
        "balancedaccuracy": [],
        "f1micro": [],
        "f1macro": [],
        "f1weighted": [],
        "precisionmicro": [],
        "precisionmacro": [],
        "precisionweighted": [],
        "recallmicro": [],
        "recallmacro": [],
        "recallweighted": [],
        "jaccardmicro": [],
        "jaccardmacro": [],
        "jaccardweighted": [],
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
    results["balancedaccuracy"].append(
        round(float(df["balanced_accuracy"].iloc[0]) * 100, 2)
    )
    results["f1micro"].append(round(float(df["f1_micro"].iloc[0]) * 100, 2))
    results["f1macro"].append(round(float(df["f1_macro"].iloc[0]) * 100, 2))
    results["f1weighted"].append(round(float(df["f1_weighted"].iloc[0]) * 100, 2))
    results["precisionmicro"].append(
        round(float(df["precision_micro"].iloc[0]) * 100, 2)
    )
    results["precisionmacro"].append(
        round(float(df["precision_macro"].iloc[0]) * 100, 2)
    )
    results["precisionweighted"].append(
        round(float(df["precision_weighted"].iloc[0]) * 100, 2)
    )
    results["recallmicro"].append(round(float(df["recall_micro"].iloc[0]) * 100, 2))
    results["recallmacro"].append(round(float(df["recall_macro"].iloc[0]) * 100, 2))
    results["recallweighted"].append(
        round(float(df["recall_weighted"].iloc[0]) * 100, 2)
    )
    results["jaccardmicro"].append(round(float(df["jaccard_micro"].iloc[0]) * 100, 2))
    results["jaccardmacro"].append(round(float(df["jaccard_macro"].iloc[0]) * 100, 2))
    results["jaccardweighted"].append(
        round(float(df["jaccard_weighted"].iloc[0]) * 100, 2)
    )


def sort(df: pd.DataFrame):
    """
    Sorts the dataframe by all columns.

    Parameters
    ----------
    df : pd.DataFrame
        The dataframe to be sorted
    """
    df.sort_values(
        by=[
            "accuracy",
            "balancedaccuracy",
            "f1micro",
            "f1macro",
            "f1weighted",
            "precisionmicro",
            "precisionmacro",
            "precisionweighted",
            "recallmicro",
            "recallmacro",
            "recallweighted",
            "jaccardmicro",
            "jaccardmacro",
            "jaccardweighted",
            "method",
        ],
        inplace=True,
        ascending=[
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            True,
        ],
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
        sort(results_df)
        results_df.to_csv(args.output, index=False, float_format="%.2f", na_rep=".")


if __name__ == "__main__":  # pragma: no cover
    main()
