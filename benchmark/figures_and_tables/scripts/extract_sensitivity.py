import argparse
import sys
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
        description="Create boxplot for hierarchical f-score"
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
groups = {
    "sp_rdp_its.90": "A",
    "sp_rdp_its.95": "B",
    "sp_rdp_its.97": "C",
    "sp_rdp_its.99": "D",
    "sp_rdp_its.100": "E",
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


def main():  # pragma: no cover
    """Get sensitivity from TAXXI metrics."""
    args = parse_args(sys.argv[1:])
    methods = get_methods(args.taxxi_metrics)
    with open(args.output, "w") as fout:
        fout.write("Method,TPR,Group\n")
        for dataset in args.datasets:
            for method in methods:
                file = f"{args.taxxi_metrics}/{method}/{dataset}/{ranks[dataset]}.tsv"
                if exists(file):
                    with open(file, "r") as fin:
                        line = fin.readline()
                        sensitivity = line.split("\t")[-1].strip()
                        if float(sensitivity) > 11:
                            fout.write(
                                f"{pretty_name[method]},{sensitivity},{groups[dataset]}\n"
                            )
                        else:
                            fout.write(
                                f"{pretty_name[method]} ({sensitivity}),{sensitivity},{groups[dataset]}\n"
                            )


if __name__ == "__main__":  # pragma: no cover
    main()
