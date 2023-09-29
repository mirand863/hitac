from os.path import exists

import pandas as pd
import yaml


with open("config.yml", "r") as file:
    config = yaml.safe_load(file)
    ranks = config["ranks"]
    datasets = config["datasets"]
    methods = config["methods"]
    rank_map = {
        "p": "phylum",
        "c": "class",
        "o": "order",
        "f": "family",
        "g": "genus",
        "s": "species",
    }
    for dataset in datasets:
        with pd.ExcelWriter(f"results/ml_metrics/{dataset}.xlsx") as writer:
            for rank in ranks:
                metrics = []
                for method in methods:
                    file = f"results/ml_metrics/{method}/{dataset}/{rank}.tsv"
                    if exists(file):
                        metrics.append(
                            pd.read_csv(file, sep="\t")
                            .rename(columns={"value": method})
                            .set_index("metric")
                        )
                sheet = metrics[0].copy().join(metrics[1:])
                sheet.to_excel(writer, sheet_name=rank_map[rank])
