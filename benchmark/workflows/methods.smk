configfile: "config.yml"

workdir: config["workdir"]

include: "../rules/download_rdp"
include: "../rules/download_spingo"
include: "../rules/extract_rdp"
include: "../rules/extract_spingo"
include: "../rules/download_datasets.smk"
include: "../rules/download_scripts.smk"
include: "../rules/utax2qiime.smk"
include: "../rules/qiime_import.smk"
include: "../rules/blca.smk"
include: "../rules/btop.smk"
include: "../rules/ct1.smk"
include: "../rules/ct2"
include: "../rules/hitac.smk"
include: "../rules/hitac_filter"
include: "../rules/knn"
include: "../rules/ktop"
include: "../rules/metaxa2"
include: "../rules/microclass"
include: "../rules/nbc"
include: "../rules/q1"
include: "../rules/q2blast"
include: "../rules/q2sk"
include: "../rules/q2vs"
include: "../rules/rdp"
include: "../rules/sintax"
include: "../rules/spingo"
include: "../rules/top"

rule all:
    input:
        predictions = expand(
            "results/predictions/{dataset}/{method}.tsv",
            dataset=config["datasets"],
            method=config["methods"]
        )
