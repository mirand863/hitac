configfile: "config.yml"

workdir: config["workdir"]

include: "../rules/download_datasets.smk"
include: "../rules/download_scripts.smk"
include: "../rules/qiime2.smk"
include: "../rules/blca.smk"
include: "../rules/btop.smk"
include: "../rules/ct1.smk"
include: "../rules/ct2.smk"
include: "../rules/hitac.smk"
include: "../rules/hitac_filter.smk"
include: "../rules/knn.smk"
include: "../rules/ktop.smk"
include: "../rules/metaxa2"
include: "../rules/microclass.smk"
include: "../rules/nbc.smk"
include: "../rules/q1"
include: "../rules/q2blast"
include: "../rules/q2sk"
include: "../rules/q2vs.smk"
include: "../rules/rdp.smk"
include: "../rules/sintax.smk"
include: "../rules/spingo.smk"
include: "../rules/top.smk"

rule all:
    input:
        predictions = expand(
            "results/predictions/{dataset}/{method}.tsv",
            dataset=config["datasets"],
            method=config["methods"]
        )
