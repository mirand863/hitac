rule train_hitac_filter_standalone:
    input:
        reference = "data/train/{dataset}.fasta"
    output:
        filter = temp("results/temp/{dataset}/{penalty}/hitac_filter_standalone/classifier.pkl")
    benchmark:
        repeat("results/benchmark/{dataset}/{penalty}/train/hitac_filter_standalone.tsv",config["benchmark"]["repeat"])
    threads:
        config["threads"]
    conda:
        "../envs/hitac_tuning.yml"
    log:
        "results/logs/{dataset}_{penalty}_train_hitac_filter_standalone.txt"
    shell:
        """
        timeout 48h \
        hitac-fit-filter \
            --reference {input.reference} \
            --kmer 6 \
            --threads {threads} \
            --penalty {wildcards.penalty} \
            --filter {output.filter} \
            > {log} 2>&1
        """


rule classify_hitac_filter_standalone:
    input:
        query = "data/test/{dataset}.fasta",
        unfiltered_predictions = "results/predictions/{dataset}/{penalty}/hitac_standalone.tsv",
        filter = "results/temp/{dataset}/{penalty}/hitac_filter_standalone/classifier.pkl"
    output:
        filtered_predictions = "results/predictions/{dataset}/{penalty}/hitac_filter_standalone.tsv"
    benchmark:
        repeat("results/benchmark/{dataset}/{penalty}/classify/hitac_filter_standalone.tsv",config["benchmark"]["repeat"])
    threads:
        config["threads"]
    conda:
        "../envs/hitac_tuning.yml"
    log:
        "results/logs/{dataset}_{penalty}_classify_hitac_filter_standalone.txt"
    shell:
        """
        hitac-filter \
            --filter {input.filter} \
            --reads {input.query} \
            --classification {input.unfiltered_predictions} \
            --threshold 0.7 \
            --kmer 6 \
            --threads {threads} \
            --filtered-classification {output.filtered_predictions} \
            > {log} 2>&1
        """
