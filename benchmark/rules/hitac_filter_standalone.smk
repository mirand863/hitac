rule train_hitac_filter_standalone:
    input:
        reference = "data/train/{dataset}.fasta"
    output:
        filter = temp("results/temp/{dataset}/{penalty}/{solver}/hitac_filter_standalone/classifier.pkl")
    benchmark:
        repeat("results/benchmark/{dataset}/{penalty}/{solver}/train/hitac_filter_standalone.tsv",config["benchmark"]["repeat"])
    threads:
        config["threads"]
    container:
        config["containers"]["hitac_standalone"]
    log:
        "results/logs/{dataset}_{penalty}_{solver}_train_hitac_filter_sstandalone.txt"
    shell:
        """
        timeout 24h \
        hitac-fit-filter \
            --reference {input.reference} \
            --kmer 6 \
            --threads {threads} \
            --penalty {wildcards.penalty} \
            --solver {wildcards.solver} \
            --filter {output.filter} \
            > {log} 2>&1s
        """


rule classify_hitac_filter_standalone:
    input:
        query = "data/test/{dataset}.fasta",
        unfiltered_predictions = "results/predictions/{dataset}/{penalty}/{solver}/hitac_standalone.tsv",
        filter = "results/temp/{dataset}/{penalty}/{solver}/hitac_filter_standalone/classifier.pkl"
    output:
        filtered_predictions = "results/predictions/{dataset}/{penalty}/{solver}/hitac_filter_standalone.tsv"
    benchmark:
        repeat("results/benchmark/{dataset}/{penalty}/{solver}/classify/hitac_filter_standalone.tsv",config["benchmark"]["repeat"])
    threads:
        config["threads"]
    container:
        config["containers"]["hitac_standalone"]
    log:
        "results/logs/{dataset}_{penalty}_{solver}_classify_hitac_filter_standalone.txt"
    shell:
        """
        timeout 1h \
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
