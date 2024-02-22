import argparse
import matplotlib
import pandas as pd
import seaborn as sns
import sys
from argparse import Namespace
from glob import glob
from matplotlib import pyplot as plt
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
        description="Create bar plot for hierarchical metrics"
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


def merge_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Merge precision, recall and f1-score columns.

    Parameters
    ----------
    df : pd.DataFrame
        Dataframe containing precision, recall and f1-score.

    Returns
    -------
    df : pd.DataFrame
        Dataframe containing merged precision, recall and f1.
    """
    results = {
        "method": [],
        "metric": [],
        "result": [],
    }
    for i in df.index:
        results["method"].append(df["method"][i])
        results["method"].append(df["method"][i])
        results["method"].append(df["method"][i])
        results["metric"].append("F1-score")
        results["metric"].append("Precision")
        results["metric"].append("Recall")
        results["result"].append(df["f1"][i])
        results["result"].append(df["precision"][i])
        results["result"].append(df["recall"][i])
    return pd.DataFrame(data=results)


def plot(df: pd.DataFrame, output: str) -> None:
    """
    Draw a nested barplot from the hierarchical metrics.

    Parameters
    ----------
    df : pd.DataFrame
        Dataframe containing the hierarchical metrics.
    output : str
        Output file to write PDF.

    Returns
    -------

    """
    sns.set_theme(style="whitegrid")
    g = sns.catplot(
        data=df,
        kind="bar",
        x="result",
        y="method",
        hue="metric",
        errorbar="sd",
        palette=["#001219", "#0A9396", "#AE2012"],
        height=6,
        orient="h",
    )
    g.despine(left=True)
    g.set_axis_labels("", "")
    g.legend.set_title("")
    plt.show()
    plt.savefig(
        output,
        bbox_inches="tight",
    )


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
    "method": [],
    "precision": [],
    "recall": [],
    "f1": [],
}


def main():  # pragma: no cover
    """Generate bar plot for hierarchical metrics."""
    args = parse_args(sys.argv[1:])
    methods = get_methods(args.hierarchical_metrics, args.dataset)
    for method in methods:
        file = f"results/hierarchical_metrics/{method}/{args.dataset}.tsv"
        if exists(file):
            df = pd.read_csv(file, sep="\t")
            results["method"].append(pretty_name[method])
            results["precision"].append(round(df["precision"].iloc[0] * 100, 2))
            results["recall"].append(round(df["recall"].iloc[0] * 100, 2))
            results["f1"].append(round(df["f1"].iloc[0] * 100, 2))
    results_df = pd.DataFrame(data=results)
    # Sort values
    results_df.sort_values(
        by=["f1", "precision", "recall", "method"],
        inplace=True,
        ascending=[False, False, False, False],
    )
    results_df.reset_index(drop=True, inplace=True)
    results_df = merge_columns(results_df)
    plot(results_df, args.output)


if __name__ == "__main__":  # pragma: no cover
    main()
