import warnings
from os.path import exists

import pandas as pd

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


for dataset in datasets:
    for rank in ranks:
        results = {
            "method": [],
            "accuracy": [],
            "balanced_accuracy": [],
            "f1_micro": [],
            "f1_macro": [],
            "f1_weighted": [],
            "precision_micro": [],
            "precision_macro": [],
            "precision_weighted": [],
            "recall_micro": [],
            "recall_macro": [],
            "recall_weighted": [],
            "jaccard_micro": [],
            "jaccard_macro": [],
            "jaccard_weighted": [],
        }
        for method in methods:
            file = f"results/ml_metrics/{method}/{dataset}/{rank}.tsv"
            if exists(file):
                df = pd.read_csv(file, sep="\t")
                accuracy = float(df["accuracy"].iloc[0])
                balanced_accuracy = float(df["balanced_accuracy"].iloc[0])
                f1_micro = float(df["f1_micro"].iloc[0])
                f1_macro = float(df["f1_macro"].iloc[0])
                f1_weighted = float(df["f1_weighted"].iloc[0])
                precision_micro = float(df["precision_micro"].iloc[0])
                precision_macro = float(df["precision_macro"].iloc[0])
                precision_weighted = float(df["precision_weighted"].iloc[0])
                recall_micro = float(df["recall_micro"].iloc[0])
                recall_macro = float(df["recall_macro"].iloc[0])
                recall_weighted = float(df["recall_weighted"].iloc[0])
                jaccard_micro = float(df["jaccard_micro"].iloc[0])
                jaccard_macro = float(df["jaccard_macro"].iloc[0])
                jaccard_weighted = float(df["jaccard_weighted"].iloc[0])
                results["method"].append(pretty_name[method])
                results["accuracy"].append(accuracy)
                results["balanced_accuracy"].append(balanced_accuracy)
                results["f1_micro"].append(f1_micro)
                results["f1_macro"].append(f1_macro)
                results["f1_weighted"].append(f1_weighted)
                results["precision_micro"].append(precision_micro)
                results["precision_macro"].append(precision_macro)
                results["precision_weighted"].append(precision_weighted)
                results["recall_micro"].append(recall_micro)
                results["recall_macro"].append(recall_macro)
                results["recall_weighted"].append(recall_weighted)
                results["jaccard_micro"].append(jaccard_micro)
                results["jaccard_macro"].append(jaccard_macro)
                results["jaccard_weighted"].append(jaccard_weighted)
        results_df = pd.DataFrame(data=results)
        # sort values
        results_df.sort_values(
            by=["accuracy"],
            inplace=True,
            ascending=[False],
        )

        # multiply values by 100 to standardize
        results_df["accuracy"] = results_df["accuracy"].apply(
            lambda x: round(x * 100, 2)
        )
        results_df["balanced_accuracy"] = results_df["balanced_accuracy"].apply(
            lambda x: round(x * 100, 2)
        )
        results_df["f1_micro"] = results_df["f1_micro"].apply(
            lambda x: round(x * 100, 2)
        )
        results_df["f1_macro"] = results_df["f1_macro"].apply(
            lambda x: round(x * 100, 2)
        )
        results_df["f1_weighted"] = results_df["f1_weighted"].apply(
            lambda x: round(x * 100, 2)
        )
        results_df["precision_micro"] = results_df["precision_micro"].apply(
            lambda x: round(x * 100, 2)
        )
        results_df["precision_macro"] = results_df["precision_macro"].apply(
            lambda x: round(x * 100, 2)
        )
        results_df["precision_weighted"] = results_df["precision_weighted"].apply(
            lambda x: round(x * 100, 2)
        )
        results_df["recall_micro"] = results_df["recall_micro"].apply(
            lambda x: round(x * 100, 2)
        )
        results_df["recall_macro"] = results_df["recall_macro"].apply(
            lambda x: round(x * 100, 2)
        )
        results_df["recall_weighted"] = results_df["recall_weighted"].apply(
            lambda x: round(x * 100, 2)
        )
        results_df["jaccard_micro"] = results_df["jaccard_micro"].apply(
            lambda x: round(x * 100, 2)
        )
        results_df["jaccard_macro"] = results_df["jaccard_macro"].apply(
            lambda x: round(x * 100, 2)
        )
        results_df["jaccard_weighted"] = results_df["jaccard_weighted"].apply(
            lambda x: round(x * 100, 2)
        )

        print(
            results_df.to_latex(
                index=False,
                bold_rows=True,
                label=f"ml:{dataset}:{pretty_ranks[rank]}",
                caption=f"Machine learning metrics computed for the dataset {pretty_datasets[dataset]} at the {pretty_ranks[rank]} level.",
            )
        )
