rule train_hitac_standalone:
    input:
        reference = "data/train/{dataset}.fasta"
    output:
        classifier = temp("results/temp/{dataset}/{penalty}/{solver}/hitac_standalone/classifier.pkl")
    benchmark:
        repeat("results/benchmark/{dataset}/{penalty}/{solver}/train/hitac_standalone.tsv",config["benchmark"]["repeat"])
    threads:
        config["threads"]
    log:
        "results/logs/{dataset}_{penalty}_{solver}_train_hitac_standalone.txt"
    conda:
        "../envs/hitac_tuning.yml"
    shell:
        """
        timeout 72h \
        hitac-fit \
            --reference {input.reference} \
            --kmer 6 \
            --threads {threads} \
            --penalty {wildcards.penalty} \
            --solver {wildcards.solver} \
            --classifier {output.classifier} \
            > {log} 2>&1
        """


rule classify_hitac_standalone:
    input:
        query = "data/test/{dataset}.fasta",
        classifier = "results/temp/{dataset}/{penalty}/{solver}/hitac_standalone/classifier.pkl"
    output:
        predictions = "results/predictions/{dataset}/{penalty}/{solver}/hitac_standalone.tsv"
    benchmark:
        repeat("results/benchmark/{dataset}/{penalty}/{solver}/classify/hitac_standalone.tsv",config["benchmark"]["repeat"])
    threads:
        config["threads"]
    log:
        "results/logs/{dataset}_{penalty}_{solver}_classify_hitac_standalone.txt"
    conda:
        "../envs/hitac_tuning.yml"
    shell:
        """
        timeout 1h \
        hitac-classify \
            --reads {input.query} \
            --classifier {input.classifier} \
            --kmer 6 \
            --threads {threads} \
            --classification {output.predictions} \
            > {log} 2>&1
        """
