from os.path import exists

import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

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

for dataset in datasets:
    results = {
        "method": [],
        "f1": [],
        "precision": [],
        "recall": [],
    }
    for method in methods:
        file = f"results/hierarchical_metrics/{method}/{dataset}.tsv"
        if exists(file):
            df = pd.read_csv(file, sep="\t")
            f1 = df["f1"].iloc[0]
            precision = df["precision"].iloc[0]
            recall = df["recall"].iloc[0]
            results["method"].append(pretty_name[method])
            results["f1"].append(f1)
            results["precision"].append(precision)
            results["recall"].append(recall)
    results_df = pd.DataFrame(data=results)

    # sort values
    results_df.sort_values(
        by=["f1"],
        inplace=True,
        ascending=[False],
    )

    # multiply values by 100 to standardize
    results_df["f1"] = results_df["f1"].apply(lambda x: round(x * 100, 2))
    results_df["precision"] = results_df["precision"].apply(lambda x: round(x * 100, 2))
    results_df["recall"] = results_df["recall"].apply(lambda x: round(x * 100, 2))

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
            label=f"hierarchical:{dataset}",
            caption=f"Hierarchical metrics computed for the dataset {pretty_datasets[dataset]}.",
        )
    )
