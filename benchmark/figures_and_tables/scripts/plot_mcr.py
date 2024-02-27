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


ranks = {
    "sp_rdp_its.90": "g",
    "sp_rdp_its.95": "g",
    "sp_rdp_its.97": "g",
    "sp_rdp_its.99": "s",
    "sp_rdp_its.100": "s",
}

subplot_title = {
    "sp_rdp_its.90": "SP RDP ITS 90\ngenus level",
    "sp_rdp_its.95": "SP RDP ITS 95\ngenus level",
    "sp_rdp_its.97": "SP RDP ITS 97\ngenus level",
    "sp_rdp_its.99": "SP RDP ITS 99\nspecies level",
    "sp_rdp_its.100": "SP RDP ITS 100\nspecies level",
}

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


def plot(df: pd.DataFrame, output) -> None:
    fig = plt.figure(figsize=(8.3, 11.7))
    axs = [None] * 5
    plt.subplots_adjust(wspace=0.05, hspace=0)
    plt.rc("font", weight="bold")
    width = 0.4  # the width of the bars
    sp_rdp_its_90 = df[df["Dataset"] == "sp_rdp_its.90"]
    sp_rdp_its_90.reset_index(drop=True, inplace=True)
    y = np.arange(len(sp_rdp_its_90["Method"]))  # Label locations
    axs[0] = fig.add_subplot(151, axes_class=axisartist.Axes)
    axs[0].barh(y, sp_rdp_its_90["MCR"], width + 0.2, label="MCR", color="#001219")
    axs[0].set_yticklabels(sp_rdp_its_90["Method"])
    axs[0].set(xlim=(min(df["MCR"]), max(df["MCR"])), ylim=(min(y) - 1, max(y) + 1))
    axs[0].set_xticks([])
    axs[0].set_yticks(y)
    axs[0].axis["left"].major_ticklabels.set_ha("left")
    axs[0].set_title(subplot_title["sp_rdp_its.90"], fontweight="bold", fontsize="10")
    axs[0].axis["top"].set_visible(False)
    axs[0].axis["right"].set_visible(False)
    axs[0].axis["bottom"].set_visible(False)
    # axs[0].axis["left"].set_visible(False)  # this also erases the labels
    for i, v in enumerate(sp_rdp_its_90["MCR"].to_numpy()):
        if v >= 6:
            axs[0].text(
                0.1,
                i,
                str(v),
                color="white",
                fontweight="bold",
                verticalalignment="center",
            )
        else:
            axs[0].text(
                v,
                i,
                str(v),
                color="black",
                fontweight="bold",
                verticalalignment="center",
            )
    sp_rdp_its_95 = df[df["Dataset"] == "sp_rdp_its.95"]
    axs[1] = fig.add_subplot(152, axes_class=axisartist.Axes)
    axs[1].barh(
        y, sp_rdp_its_95["MCR"].to_numpy(), width + 0.2, label="MCR", color="#005F73"
    )
    axs[1].set(xlim=(min(df["MCR"]), max(df["MCR"])), ylim=(min(y) - 1, max(y) + 1))
    axs[1].set_xticks([])
    axs[1].set_yticks([])
    axs[1].set_title(subplot_title["sp_rdp_its.95"], fontweight="bold", fontsize="10")
    axs[1].axis["top"].set_visible(False)
    axs[1].axis["right"].set_visible(False)
    axs[1].axis["bottom"].set_visible(False)
    axs[1].axis["left"].set_visible(False)
    for i, v in enumerate(sp_rdp_its_95["MCR"].to_numpy()):
        if v >= 6:
            axs[1].text(
                0.1,
                i,
                str(v),
                color="white",
                fontweight="bold",
                verticalalignment="center",
            )
        else:
            axs[1].text(
                v,
                i,
                str(v),
                color="black",
                fontweight="bold",
                verticalalignment="center",
            )
    sp_rdp_its_97 = df[df["Dataset"] == "sp_rdp_its.97"]
    axs[2] = fig.add_subplot(153, axes_class=axisartist.Axes)
    axs[2].barh(
        y, sp_rdp_its_97["MCR"].to_numpy(), width + 0.2, label="MCR", color="#EE9B00"
    )
    axs[2].set(xlim=(min(df["MCR"]), max(df["MCR"])), ylim=(min(y) - 1, max(y) + 1))
    axs[2].set_xticks([])
    axs[2].set_yticks([])
    axs[2].set_title(subplot_title["sp_rdp_its.97"], fontweight="bold", fontsize="10")
    axs[2].axis["top"].set_visible(False)
    axs[2].axis["right"].set_visible(False)
    axs[2].axis["bottom"].set_visible(False)
    axs[2].axis["left"].set_visible(False)
    for i, v in enumerate(sp_rdp_its_97["MCR"].to_numpy()):
        if v >= 6:
            axs[2].text(
                0.1,
                i,
                str(v),
                color="white",
                fontweight="bold",
                verticalalignment="center",
            )
        else:
            axs[2].text(
                v,
                i,
                str(v),
                color="black",
                fontweight="bold",
                verticalalignment="center",
            )
    sp_rdp_its_99 = df[df["Dataset"] == "sp_rdp_its.99"]
    axs[3] = fig.add_subplot(154, axes_class=axisartist.Axes)
    axs[3].barh(
        y, sp_rdp_its_99["MCR"].to_numpy(), width + 0.2, label="MCR", color="#CA6702"
    )
    axs[3].set(xlim=(min(df["MCR"]), max(df["MCR"])), ylim=(min(y) - 1, max(y) + 1))
    axs[3].set_xticks([])
    axs[3].set_yticks([])
    axs[3].set_title(subplot_title["sp_rdp_its.99"], fontweight="bold", fontsize="10")
    axs[3].axis["top"].set_visible(False)
    axs[3].axis["right"].set_visible(False)
    axs[3].axis["bottom"].set_visible(False)
    axs[3].axis["left"].set_visible(False)
    for i, v in enumerate(sp_rdp_its_99["MCR"].to_numpy()):
        if v >= 6:
            axs[3].text(
                0.1,
                i,
                str(v),
                color="white",
                fontweight="bold",
                verticalalignment="center",
            )
        else:
            axs[3].text(
                v,
                i,
                str(v),
                color="black",
                fontweight="bold",
                verticalalignment="center",
            )
    sp_rdp_its_100 = df[df["Dataset"] == "sp_rdp_its.100"]
    axs[4] = fig.add_subplot(155, axes_class=axisartist.Axes)
    axs[4].barh(
        y, sp_rdp_its_100["MCR"].to_numpy(), width + 0.2, label="MCR", color="#9B2226"
    )
    axs[4].set(xlim=(min(df["MCR"]), max(df["MCR"])), ylim=(min(y) - 1, max(y) + 1))
    axs[4].set_xticks([])
    axs[4].set_yticks([])
    axs[4].set_title(subplot_title["sp_rdp_its.100"], fontweight="bold", fontsize="10")
    axs[4].axis["top"].set_visible(False)
    axs[4].axis["right"].set_visible(False)
    axs[4].axis["bottom"].set_visible(False)
    axs[4].axis["left"].set_visible(False)
    for i, v in enumerate(sp_rdp_its_100["MCR"].to_numpy()):
        if v >= 6:
            axs[4].text(
                0.1,
                i,
                str(v),
                color="white",
                fontweight="bold",
                verticalalignment="center",
            )
        elif math.isnan(v):
            axs[4].text(
                1,
                i,
                "Memory\nexceeded",
                color="black",
                fontweight="bold",
                verticalalignment="center",
            )
        else:
            axs[4].text(
                v,
                i,
                str(v),
                color="black",
                fontweight="bold",
                verticalalignment="center",
            )
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
            file = f"{args.taxxi_metrics}/{method}/{dataset}/{ranks[dataset]}.tsv"
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
