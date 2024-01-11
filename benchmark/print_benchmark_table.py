import argparse
import sys
from argparse import Namespace
from copy import deepcopy
from glob import glob
from typing import TextIO, List

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
        description="Get accuracy results for selected datasets and taxonomic ranks"
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
        default="results/benchmark/sp_rdp_its_100.txt",
        help="Output to write results [default: results/benchmark/sp_rdp_its_100.txt]",
    )
    return parser.parse_args(args)


def get_methods(benchmark_folder: str, dataset: str) -> List[str]:
    """
    Return all methods with Acc set to NaN.

    Parameters
    ----------
    benchmark_folder : str
        Path to the metrics folder.
    dataset : str
        Dataset to extract benchmark results.

    Returns
    -------
    methods : List[str]
        Methods in benchmark folder.
    """
    paths = glob(f"{benchmark_folder}/{dataset}/*", recursive=True)
    methods = [method.split("/")[-1].replace(".tsv", "") for method in paths]
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


def compute_time(benchmark_folder: str, dataset: str, method: str) -> str:
    """
    Compute average time spent by a method from a Snakemake benchmark TSV file.

    Parameters
    ----------
    benchmark_folder : str
        Path to the metrics folder.
    dataset : str
        Dataset to extract benchmark results.
    method : str
        The TSV file containing benchmarking results.

    Returns
    -------
    time : str
        The average time in hh:mm:ss.
    """
    file = f"{benchmark_folder}/{dataset}/{method}.tsv"
    df = pd.read_csv(file, sep="\t", usecols=["s"])
    average_time = df["s"].mean()
    hours = add_zero(average_time / 3600)
    average_time = average_time % 3600
    minutes = add_zero(average_time / 60)
    average_time = add_zero(average_time % 60)
    time = f"{hours}:{minutes}:{average_time}"
    return time


def compute_memory(benchmark_folder: str, dataset: str, method: str) -> float:
    """
    Compute average memory spent by a method from a Snakemake benchmark TSV file.

    Parameters
    ----------
    benchmark_folder : str
        Path to the metrics folder.
    dataset : str
        Dataset to extract benchmark results.
    method : str
        The TSV file containing benchmarking results.

    Returns
    -------
    memory : float
        The average memory.
    """
    file = f"{benchmark_folder}/{dataset}/{method}.tsv"
    df = pd.read_csv(file, sep="\t", usecols=["max_rss"])
    memory = df["max_rss"].mean()
    return round(memory, 2)


pretty_name = {
    "q2vs": r"Q2\_VS",
    "sintax": "SINTAX",
    "btop": "BTOP",
    "microclass": "Microclass",
    "spingo": "SPINGO",
    "knn": "KNN",
    "q1": "Q1",
    "hitac_qiime": "HiTaC\_QIIME",
    "hitac_standalone": "HiTaC\_standalone",
    "q2sk": r"Q2\_SK",
    "nbc": "NBC",
    "rdp": "RDP",
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


def write(method: str, time: str, memory: float, output: TextIO) -> None:
    """
    Write benchmark result to output file in latex format.

    Parameters
    ----------
    method : str
        Method name.
    time : str
        CPU time.
    memory : float
        Memory usage.
    output : TextIO
        Output to write results.
    """
    output.write(f"{pretty_name[method]} & {time} & {memory} \\\\\n")


def main():  # pragma: no cover
    """Plot sunburst chart with a given taxonomy."""
    args = parse_args(sys.argv[1:])
    with open(args.output, "w") as output:
        methods = get_methods(args.benchmark, args.dataset)
        time = {}
        memory = {}
        for method in methods:
            time[method] = compute_time(args.benchmark, args.dataset, method)
            memory[method] = compute_memory(args.benchmark, args.dataset, method)
        # Sort methods according to CPU time
        time = {k: v for k, v in sorted(time.items(), key=lambda item: item[1])}
        for method in time:
            write(method, time[method], memory[method], output)


if __name__ == "__main__":  # pragma: no cover
    main()
