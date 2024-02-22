import argparse
import pandas as pd
import sys
from argparse import Namespace
from copy import deepcopy
from glob import glob
from os.path import exists
from typing import TextIO, List


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
        description="Create benchmark table for given dataset"
    )
    parser.add_argument(
        "--benchmark",
        type=str,
        required=False,
        default="results/benchmark",
        help="Folder where benchmark results are stored [default: results/benchmark]",
    )
    parser.add_argument(
        "--dataset",
        type=str,
        required=False,
        default="sp_rdp_its.100",
        help="Dataset to compute metrics [default: sp_rdp_its.100]",
    )
    parser.add_argument(
        "--output",
        type=str,
        required=False,
        default="results/figures_and_tables/benchmarks/sp_rdp_its_100.txt",
        help="Output to write results [default: results/figures_and_tables/benchmarks/sp_rdp_its_100.txt]",
    )
    return parser.parse_args(args)


def get_methods(benchmark_folder: str, dataset: str) -> List[str]:
    """
    Return all methods names.

    Parameters
    ----------
    benchmark_folder : str
        Path to the benchmark folder.
    dataset : str
        Dataset to extract benchmark results.

    Returns
    -------
    methods : List[str]
        Methods in benchmark folder.
    """
    paths = glob(f"{benchmark_folder}/{dataset}/*/*", recursive=True)
    methods = [path.split("/")[-1].replace(".tsv", "") for path in paths]
    methods = list(set(methods))
    # methods.remove("hitac_filter_qiime")
    # methods.remove("hitac_qiime")
    methods.sort()
    return methods


def add_zero(number: int) -> str:
    """
    Add zero in the beginning, if there is only one character.

    Parameters
    ----------
    number : int
        Value to possibly add zeros.

    Returns
    -------
    number_with_zeros : str
        Corrected number.
    """
    number_with_zeros = str(int(number))
    while len(number_with_zeros) < 2:
        number_with_zeros = "0" + number_with_zeros
    return number_with_zeros


def compute_time(
    benchmark_folder: str, train_or_classify: str, dataset: str, method: str
) -> str:
    """
    Compute average time spent by a method from a Snakemake benchmark TSV file.

    Parameters
    ----------
    benchmark_folder : str
        Path to the metrics folder.
    train_or_classify : str
        Distinguish between training or classification benchmarks.
    dataset : str
        Dataset to extract benchmark results.
    method : str
        The TSV file containing benchmarking results.

    Returns
    -------
    time : str
        The average time in hh:mm:ss.
    """
    file = f"{benchmark_folder}/{dataset}/{train_or_classify}/{method}.tsv"
    if exists(file):
        df = pd.read_csv(file, sep="\t", usecols=["s"])
        average_time = df["s"].mean()
        hours = add_zero(average_time / 3600)
        average_time = average_time % 3600
        minutes = add_zero(average_time / 60)
        average_time = add_zero(average_time % 60)
        time = f"{hours}:{minutes}:{average_time}"
        return time
    else:
        return "nan"


def compute_memory(
    benchmark_folder: str, train_or_classify: str, dataset: str, method: str
) -> float:
    """
    Compute average memory spent by a method from a Snakemake benchmark TSV file.

    Parameters
    ----------
    benchmark_folder : str
        Path to the metrics folder.
    train_or_classify : str
        Distinguish between training or classification benchmarks.
    dataset : str
        Dataset to extract benchmark results.
    method : str
        The TSV file containing benchmarking results.

    Returns
    -------
    memory : float
        The average memory.
    """
    file = f"{benchmark_folder}/{dataset}/{train_or_classify}/{method}.tsv"
    if exists(file):
        df = pd.read_csv(file, sep="\t", usecols=["max_rss"])
        memory = df["max_rss"].mean()
        return round(memory, 2)
    else:
        return "nan"


pretty_name = {
    "q2vs": r"Q2_VS",
    "sintax": "SINTAX",
    "btop": "BTOP",
    "microclass": "Microclass",
    "spingo": "SPINGO",
    "knn": "KNN",
    "q1": "Q1",
    "hitac_standalone": "HiTaC",
    "q2sk": r"Q2_SK",
    "nbc": "NBC",
    "rdp": "RDP",
    "ct2": "CT2",
    "metaxa2": "Metaxa2",
    "ktop": "KTOP",
    "top": "TOP",
    "hitac_filter_standalone": r"HiTaC_Filter",
    "q2blast": r"Q2_BLAST",
    "blca": "BLCA",
    "ct1": "CT1",
}
pretty_datasets = {
    "sp_rdp_its.90": "SP RDP ITS 90",
    "sp_rdp_its.95": "SP RDP ITS 95",
    "sp_rdp_its.97": "SP RDP ITS 97",
    "sp_rdp_its.99": "SP RDP ITS 99",
    "sp_rdp_its.100": "SP RDP ITS 100",
}


def main():  # pragma: no cover
    """Generate benchmark tables."""
    args = parse_args(sys.argv[1:])
    with open(args.output, "w") as output:
        methods = get_methods(args.benchmark, args.dataset)
        results = {
            "Method": [],
            "Training Time": [],
            "Training Memory": [],
            "Classification Time": [],
            "Classification Memory": [],
        }
        for method in methods:
            training_time = compute_time(args.benchmark, "train", args.dataset, method)
            classification_time = compute_time(
                args.benchmark, "classify", args.dataset, method
            )
            training_memory = compute_memory(
                args.benchmark, "train", args.dataset, method
            )
            classification_memory = compute_memory(
                args.benchmark, "classify", args.dataset, method
            )
            results["Method"].append(pretty_name[method])
            results["Training Time"].append(training_time)
            results["Training Memory"].append(training_memory)
            results["Classification Time"].append(classification_time)
            results["Classification Memory"].append(classification_memory)
        results_df = pd.DataFrame(data=results)
        # Sort methods according to CPU training time
        results_df.sort_values(
            by=["Training Time"],
            inplace=True,
            ascending=[True],
        )
        # Write results
        output.write(
            results_df.to_latex(
                index=False,
                bold_rows=True,
                label=f"benchmark:{args.dataset}",
                caption=f"Results obtained by the resources benchmark for the dataset {pretty_datasets[args.dataset]}.",
            )
        )


if __name__ == "__main__":  # pragma: no cover
    main()
