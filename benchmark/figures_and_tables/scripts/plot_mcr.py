import argparse
import math
import sys
from argparse import Namespace
from glob import glob
from os.path import exists
from typing import List

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt, gridspec
from matplotlib.patches import ConnectionPatch
from mpl_toolkits import axisartist


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
        description="Plot the misclassification rate for multiple datasets"
    )
    parser.add_argument(
        "--taxxi-metrics",
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
    taxxi_folder: str,
) -> List[str]:
    """
    Return all methods names.

    Parameters
    ----------
    taxxi_folder : str
        Path to the metrics folder.

    Returns
    -------
    methods : List[str]
        Methods in metrics folder.
    """
    paths = glob(f"{taxxi_folder}/*/*/*.tsv", recursive=True)
    methods = [path.split("/")[2] for path in paths]
    methods = list(set(methods))
    methods.remove("hitac_filter_qiime")
    methods.remove("hitac_qiime")
    methods.sort()
    return methods


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
    "Dataset": [],
    "MCR": [],
}

metadata = {
    "sp_rdp_its.90": {
        "rank": "g",
        "subplot_title": "SP RDP ITS 90\ngenus level",
        "bar_color": "#001219",
        "grid": 151,
    },
    "sp_rdp_its.95": {
        "rank": "g",
        "subplot_title": "SP RDP ITS 95\ngenus level",
        "bar_color": "#005F73",
        "grid": 152,
    },
    "sp_rdp_its.97": {
        "rank": "g",
        "subplot_title": "SP RDP ITS 97\ngenus level",
        "bar_color": "#EE9B00",
        "grid": 153,
    },
    "sp_rdp_its.99": {
        "rank": "s",
        "subplot_title": "SP RDP ITS 99\nspecies level",
        "bar_color": "#CA6702",
        "grid": 154,
    },
    "sp_rdp_its.100": {
        "rank": "s",
        "subplot_title": "SP RDP ITS 100\nspecies level",
        "bar_color": "#9B2226",
        "grid": 155,
    },
}


def subplot(
    df: pd.DataFrame, dataset: str, fig: plt.figure, y: np.ndarray, width: float
):
    """
    Plot a subplot.

    Parameters
    ----------
    df : pd.DataFrame
        The dataframe containing the data.
    dataset : str
        The name of the dataset to plot.
    fig : plt.figure
        The matplotlib figure to plot the subplot.
    y : np.ndarray
        Locations of labels.
    width : The width of the bar in the subplot.

    Returns
    -------
    ax : matplotlib.axes.Axis
        The axis instance the artist resides in.
    """
    subset = df[df["Dataset"] == dataset]
    ax = fig.add_subplot(metadata[dataset]["grid"], axes_class=axisartist.Axes)
    ax.barh(
        y, subset["MCR"], width + 0.2, label="MCR", color=metadata[dataset]["bar_color"]
    )
    ax.set(xlim=(min(df["MCR"]), max(df["MCR"])), ylim=(min(y) - 1, max(y) + 1))
    ax.set_xticks([])
    ax.set_yticks(y)
    ax.set_yticklabels(subset["Method"])
    ax.axis["left"].major_ticklabels.set_ha("left")
    ax.set_title(metadata[dataset]["subplot_title"], fontweight="bold", fontsize="10")
    ax.axis["top"].set_visible(False)
    ax.axis["right"].set_visible(False)
    ax.axis["bottom"].set_visible(False)
    if dataset != "sp_rdp_its.90":
        ax.axis["left"].set_visible(False)  # this also erases the labels
    for i, v in enumerate(subset["MCR"].to_numpy()):
        if v >= 6:
            ax.text(
                0.1,
                i,
                str(v),
                color="white",
                verticalalignment="center",
            )
        elif math.isnan(v):
            ax.text(
                1,
                i,
                "Memory\nexceeded",
                color="black",
                verticalalignment="center",
            )
        else:
            ax.text(
                v,
                i,
                str(v),
                color="black",
                verticalalignment="center",
            )
    return ax


def plot(df: pd.DataFrame, output: str) -> None:
    """
    Plot the miclassification rates.

    Parameters
    ----------
    df : pd.DataFrame
        The dataframe containint the results.
    output : str
        The file to save the plot.
    """
    fig = plt.figure(figsize=(8.3, 11.7))
    axs = [None] * 5
    plt.subplots_adjust(wspace=0.05, hspace=0)
    plt.rc("font", weight="bold")
    width = 0.6  # the width of the bars
    y = np.arange(22)  # Label locations
    for i, dataset in enumerate(
        [
            "sp_rdp_its.90",
            "sp_rdp_its.95",
            "sp_rdp_its.97",
            "sp_rdp_its.99",
            "sp_rdp_its.100",
        ]
    ):
        axs[i] = subplot(df, dataset, fig, y, width)
    fig.suptitle("Misclassification rate", fontweight="bold", fontsize="12", y=0.95)
    for i in range(21):
        con = ConnectionPatch(
            xyA=(0, i + 0.5),
            xyB=(max(df["MCR"]), i + 0.5),
            coordsA="data",
            coordsB="data",
            axesA=axs[0],
            axesB=axs[4],
            color="gray",
            alpha=0.4,
        )
        axs[4].add_artist(con)
    con = ConnectionPatch(
        xyA=(0, 21.5),
        xyB=(max(df["MCR"]), 21.5),
        coordsA="data",
        coordsB="data",
        axesA=axs[0],
        axesB=axs[4],
        color="black",
    )
    axs[4].add_artist(con)
    axs[0].annotate("Method", (0, 21), xytext=(-70, 45), textcoords="offset points")
    plt.savefig(
        output,
        bbox_inches="tight",
    )


def main():  # pragma: no cover
    """Plot misclassification rates from TAXXI metrics."""
    args = parse_args(sys.argv[1:])
    methods = get_methods(args.taxxi_metrics)
    for dataset in args.datasets:
        for method in methods:
            file = f"{args.taxxi_metrics}/{method}/{dataset}/{metadata[dataset]['rank']}.tsv"
            results["Method"].append(pretty_name[method])
            results["Dataset"].append(dataset)
            if exists(file):
                with open(file, "r") as fin:
                    fin.readline()
                    fin.readline()
                    line = fin.readline()
                    mcr = float(line.split("\t")[-1].strip())
                    results["MCR"].append(mcr)
            else:
                results["MCR"].append(float("nan"))
    results_df = pd.DataFrame(data=results)
    results_df.sort_values(
        by=["Dataset", "Method"],
        inplace=True,
        ascending=[True, False],
    )
    results_df.reset_index(drop=True, inplace=True)
    plot(results_df, args.output)


if __name__ == "__main__":  # pragma: no cover
    main()
