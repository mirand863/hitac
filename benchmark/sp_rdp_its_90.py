from os.path import exists

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


methods = [
    "hitac_filter_standalone",
    "hitac_standalone",
    "q2vs",
    "ct2",
    "nbc80",
    "rdp80",
    "sintax80",
    "q2blast",
    "metaxa2",
    "knn",
    "nbc50",
    "q2sk",
    # "rdp50",
    # "ct1",
    # "btop",
    # "microclass",
    # "top",
    # "ktop",
    # "blca",
    # "q1",
    # "spingo",
]
datasets = [
    "sp_rdp_its.90",
    # "sp_rdp_its.95",
    # "sp_rdp_its.97",
    # "sp_rdp_its.99",
    # "sp_rdp_its.100",
]
pretty_name = {
    "hitac_filter_standalone": "HiTaC_Filter",
    "hitac_standalone": "HiTaC",
    "q2vs": "Q2_VS",
    "ct2": "CT2",
    "nbc80": "NBC80",
    "rdp80": "RDP80",
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
    "metric": [],
    "result": [],
}
for method in methods:
    for dataset in datasets:
        file = f"results/hierarchical_metrics/{method}/{dataset}.tsv"
        if exists(file):
            df = pd.read_csv(file, sep="\t")
            precision = df["precision"].iloc[0]
            recall = df["recall"].iloc[0]
            results["method"].append(pretty_name[method])
            results["method"].append(pretty_name[method])
            results["metric"].append("Precision")
            results["metric"].append("Recall")
            results["result"].append(precision)
            results["result"].append(recall)
results_df = pd.DataFrame(data=results)

sns.set_theme(
    style="whitegrid",
    font_scale=3,
)

# Draw a nested barplot
g = sns.catplot(
    data=results_df,
    kind="bar",
    x="method",
    y="result",
    hue="metric",
    errorbar=None,
    palette="dark",
    alpha=0.8,
    # height=6,
    aspect=4,
)
g.despine(left=True)
g.set_axis_labels("", "")
g.legend.set_title("")
# g._legend.remove()
plt.ylim(0, 1)
plt.yticks([0, 0.25, 0.50, 0.75, 1], [0, 0.25, 0.50, 0.75, 1])
plt.xticks(rotation=60)
# plt.show()
plt.savefig(
    "sp_rdp_its_90.pdf",
    bbox_inches="tight",
)
print(results_df)
print(matplotlib.rcParams["font.family"])
