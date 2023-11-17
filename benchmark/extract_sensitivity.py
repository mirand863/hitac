from os.path import exists

import pandas as pd

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

with open("sensitivity.csv", "w") as fout:
    fout.write("Method,TPR,Group\n")
    for dataset in datasets:
        for method in methods:
            file = f"results/taxxi_metrics/{method}/{dataset}/{ranks[dataset]}.tsv"
            if exists(file):
                with open(file, "r") as fin:
                    line = fin.readline()
                    sensitivity = line.split("\t")[-1].strip()
                    if float(sensitivity) > 11:
                        fout.write(f"{pretty_name[method]},{sensitivity},{groups[dataset]}\n")
                    else:
                        fout.write(f"{pretty_name[method]} ({sensitivity}),{sensitivity},{groups[dataset]}\n")
