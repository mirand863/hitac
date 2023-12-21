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
    "method": [],
    "metric": [],
    "result": [],
}
for method in methods:
    for dataset in datasets:
        file = f"results/hierarchical_metrics/{method}/{dataset}.tsv"
        if exists(file):
            df = pd.read_csv(file, sep="\t")
            f1 = df["f1"].iloc[0]
            results["method"].append(pretty_name[method])
            results["metric"].append("f1")
            results["result"].append(f1)
results_df = pd.DataFrame(data=results)

print(results_df)

# titanic = sns.load_dataset('titanic')
#
# print(titanic)

# sns.boxplot(data=titanic, x="age", y="deck", width=.5)
sns.set_palette("colorblind")
g = sns.boxplot(data=results_df, x="result", y="method", whis=(0, 100))
g.set(xlabel=None)
g.set(ylabel=None)
plt.show()
plt.savefig(
    "f_score.pdf",
    bbox_inches="tight",
)
