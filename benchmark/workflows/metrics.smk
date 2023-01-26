configfile: "config.yml"

workdir: config["workdir"]

include: "../rules/download_datasets.smk"
include: "../rules/download_scripts.smk"
include: "../rules/download_namecounts.smk"
include: "../rules/compute_metrics.smk"

rule all:
    input:
        metrics = expand(
            "results/metrics/{method}/{dataset}/{rank}.tsv",
            method=config["methods"],
            dataset=config["datasets"],
            rank=config["ranks"],
        )
