configfile: "config.yml"

workdir: config["workdir"]

include: "../rules/download_blca.smk"
include: "../rules/download_usearch.smk"
include: "../rules/download_rdp.smk"
include: "../rules/download_spingo.smk"
include: "../rules/extract_blca.smk"
include: "../rules/extract_usearch.smk"
include: "../rules/extract_rdp.smk"
include: "../rules/extract_spingo.smk"
include: "../rules/download_datasets.smk"
include: "../rules/download_scripts.smk"
include: "../rules/fasta_utax2qiime.smk"
include: "../rules/blca.smk"
include: "../rules/btop.smk"
include: "../rules/ct1.smk"
include: "../rules/ct2.smk"
include: "../rules/hitac.smk"
include: "../rules/hitac_filter.smk"
include: "../rules/knn.smk"
include: "../rules/ktop.smk"
include: "../rules/metaxa2.smk"
include: "../rules/microclass.smk"
include: "../rules/nbc.smk"
include: "../rules/q1.smk"
include: "../rules/q2blast.smk"
include: "../rules/q2sk.smk"
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
