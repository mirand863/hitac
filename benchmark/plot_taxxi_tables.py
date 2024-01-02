from os.path import exists

import warnings
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

warnings.simplefilter(action="ignore", category=FutureWarning)

methods = [
    "hitac_filter_standalone",
    "hitac_standalone",
    "q2vs",
    "ct2",
    "nbc80",
    "rdp80",
    "sintax50",
    "sintax80",
    "q2blast",
    "metaxa2",
    "knn",
    "nbc50",
    "q2sk",
    "rdp50",
    "ct1",
    "btop",
    "microclass",
    "top",
    "ktop",
    "blca",
    "q1",
    "spingo",
]
datasets = [
    "sp_rdp_its.90",
    "sp_rdp_its.95",
    "sp_rdp_its.97",
    "sp_rdp_its.99",
    "sp_rdp_its.100",
]
pretty_datasets = {
    "sp_rdp_its.90": "SP RDP ITS 90",
    "sp_rdp_its.95": "SP RDP ITS 95",
    "sp_rdp_its.97": "SP RDP ITS 97",
    "sp_rdp_its.99": "SP RDP ITS 99",
    "sp_rdp_its.100": "SP RDP ITS 100",
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
ranks = [
    "p",
    "c",
    "o",
    "f",
    "g",
    "s",
]
pretty_ranks = {
    "p": "phylum",
    "c": "class",
    "o": "order",
    "f": "family",
    "g": "genus",
    "s": "species",
}


def get_value(line):
    value = line.strip().split("\t")[-1]
    if value == ".":
        return "-"
    else:
        return value


for dataset in datasets:
    for rank in ranks:
        results = {
            "method": [],
            "acc": [],
            "mcr": [],
            "ocr": [],
            "tpr": [],
            "ucr": [],
        }
        for method in methods:
            file = f"results/taxxi_metrics/{method}/{dataset}/{rank}.tsv"
            if exists(file):
                with open(file, "r") as fin:
                    tpr = get_value(fin.readline())
                    ucr = get_value(fin.readline())
                    mcr = get_value(fin.readline())
                    ocr = get_value(fin.readline())
                    acc = get_value(fin.readline())
                    results["tpr"].append(tpr)
                    results["ucr"].append(ucr)
                    results["mcr"].append(mcr)
                    results["ocr"].append(ocr)
                    results["acc"].append(acc)
                    results["method"].append(pretty_name[method])
        results_df = pd.DataFrame(data=results)
        # sort values
        results_df.sort_values(
            by=["acc"],
            inplace=True,
            ascending=[False],
        )

        results_df.rename(
            columns={
                "f1": "f-score",
            },
            inplace=True,
        )
        print(
            results_df.to_latex(
                index=False,
                bold_rows=True,
                label=f"taxxi:{dataset}:{pretty_ranks[rank]}",
                caption=f"TAXXI metrics computed for the dataset {pretty_datasets[dataset]} at the {pretty_ranks[rank]} level.",
            )
        )
