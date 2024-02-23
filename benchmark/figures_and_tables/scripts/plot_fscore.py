import argparse
import sys
from argparse import Namespace
from glob import glob
from os.path import exists
from typing import List
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt


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
        description="Create boxplot for hierarchical f-score"
    )
    parser.add_argument(
        "--hierarchical-metrics",
        type=str,
        required=True,
        help="Folder where metrics results are stored",
    )
    parser.add_argument(
        "--datasets",
        type=str,
        required=True,
        nargs="+",
        help="Datasets to plot figure",
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


def split(df: pd.DataFrame) -> pd.DataFrame:
    """
    Split dataframe by f1-score into multiple lines for plotting.

    Parameters
    ----------
    df : pd.DataFrame
        The dataframe to split.

    Returns
    -------
    df : pd.DataFrame
        A new dataframe containing all samples split into multiple lines.
    """
    results = {
        "method": [],
        "metric": [],
        "result": [],
    }
    for method, scores in zip(df["method"], df["f1"]):
        for f1 in scores:
            results["method"].append(method)
            results["metric"].append("f1")
            results["result"].append(f1)
    results_df = pd.DataFrame(data=results)
    return results_df


def plot(df: pd.DataFrame, output) -> None:
    """
    Plot f1-score in a boxplot.

    Parameters
    ----------
    df : pd.DataFrame
        The dataframe containing data to plot.
    output : str
        File to write plot in PDF format
    """
    sns.set_style("whitegrid")
    g = sns.boxplot(
        data=df,
        x="result",
        y="method",
        whis=(0, 100),
        palette="colorblind",
        hue="method",
    )
    g.set(xlabel=None)
    g.set(ylabel=None)
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
    "f1": [],
    "average": [],
}


def main():  # pragma: no cover
    """Generate bar plot for hierarchical metrics."""
    args = parse_args(sys.argv[1:])
    methods = get_methods(args.hierarchical_metrics, args.datasets[0])
    for method in methods:
        file = f"results/hierarchical_metrics/{method}/{args.datasets[0]}.tsv"
        if exists(file):
            df = pd.read_csv(file, sep="\t")
            results["method"].append(pretty_name[method])
            results["f1"].append([round(df["f1"].iloc[0] * 100, 2)])
        for dataset in args.datasets[1:]:
            file = f"results/hierarchical_metrics/{method}/{dataset}.tsv"
            if exists(file):
                df = pd.read_csv(file, sep="\t")
                results["f1"][-1].append(round(df["f1"].iloc[0] * 100, 2))
        results["average"].append(np.mean(results["f1"][-1]))
    results_df = pd.DataFrame(data=results)
    # Sort values by average f1-score
    results_df.sort_values(
        by=["average"],
        inplace=True,
        ascending=[False],
    )
    results_df = split(results_df)
    plot(results_df, args.output)


if __name__ == "__main__":  # pragma: no cover
    main()
