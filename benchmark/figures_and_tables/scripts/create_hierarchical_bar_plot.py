import argparse
import sys
from argparse import Namespace
from glob import glob
from os.path import exists
from typing import List

import matplotlib as mpl
import numpy as np
import pandas as pd
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
    # Source: https://sharkcoder.com/data-visualization/mpl-double-bar
    # Variables
    width = 0.2  # the width of the bars
    # Set fontsize for ylabels
    plt.rcParams.update({"font.size": 22})
    fig, ax = plt.subplots(figsize=(16, 16))
    plt.tight_layout()
    # Plot double bars
    y = np.arange(len(df["Method"]))  # Label locations
    ax.barh(y + 0.2, df["F1-score"], width + 0.2, label="F1-score", color="#001219")
    ax.barh(y, df["Precision"], width, label="Precision", color="#0A9396")
    ax.barh(y - 0.2, df["Recall"], width, label="Recall", color="#AE2012")
    # Format ticks
    ax.xaxis.set_major_formatter(mpl.ticker.StrMethodFormatter("{x:,.0f}"))
    # Adjust subplots
    plt.subplots_adjust(left=0.35, top=0.9)
    # Create labels
    rects = ax.patches
    for rect in rects:
        # Get X and Y placement of label from rect.
        x_value = rect.get_width()
        y_value = rect.get_y() + rect.get_height() / 2
        space = 5
        ha = "left"
        if x_value < 0:
            space *= -1
            ha = "right"
        label = "{:,.0f}".format(x_value)
        plt.annotate(
            label,
            (x_value, y_value),
            xytext=(space, 0),
            textcoords="offset points",
            va="center",
            ha=ha,
            fontsize=12,
        )
    # Set y-labels and legend
    ax.set_yticklabels(df["Method"])
    ax.legend()
    # Put legend outside plot
    plt.legend(loc=(1.02, 0))
    # Add grid lines
    plt.grid(color="black", axis="x", alpha=0.2)
    # To show each y-label, not just even ones
    plt.yticks(np.arange(min(y), max(y) + 1, 1.0))
    plt.savefig(output, bbox_inches="tight")


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
    "Precision": [],
    "Recall": [],
    "F1-score": [],
}


def main():  # pragma: no cover
    """Generate bar plot for hierarchical metrics."""
    args = parse_args(sys.argv[1:])
    methods = get_methods(args.hierarchical_metrics, args.dataset)
    for method in methods:
        file = f"results/hierarchical_metrics/{method}/{args.dataset}.tsv"
        if exists(file):
            df = pd.read_csv(file, sep="\t")
            results["Method"].append(pretty_name[method])
            results["Precision"].append(round(df["precision"].iloc[0] * 100, 2))
            results["Recall"].append(round(df["recall"].iloc[0] * 100, 2))
            results["F1-score"].append(round(df["f1"].iloc[0] * 100, 2))
    results_df = pd.DataFrame(data=results)
    # Sort values
    results_df.sort_values(
        by=["F1-score", "Precision", "Recall", "Method"],
        inplace=True,
        ascending=[True, True, True, True],
    )
    results_df.reset_index(drop=True, inplace=True)
    plot(results_df, args.output)


if __name__ == "__main__":  # pragma: no cover
    main()
