def get_mem_gb(wildcards, attempt):
    return attempt * config["slurm"]["memory_increments_gb"]


rule train_hitac_standalone:
    input:
        reference = "data/train/{dataset}.fasta"
    output:
        classifier = temp("results/temp/{dataset}/{penalty}/hitac_standalone/classifier.pkl")
    benchmark:
        repeat("results/benchmark/{dataset}/{penalty}/train/hitac_standalone.tsv",config["benchmark"]["repeat"])
    threads:
        config["threads"]
    log:
        "results/logs/{dataset}_{penalty}_train_hitac_standalone.txt"
    conda:
        "../envs/hitac_tuning.yml"
    resources:
        mem_gb=get_mem_gb,
        gpus=1,
        partition=config["slurm"]["gpu_partition"]
    shell:
        """
        timeout 48h \
        hitac-fit \
            --reference {input.reference} \
            --kmer 6 \
            --threads {threads} \
            --penalty {wildcards.penalty} \
            --classifier {output.classifier} \
            > {log} 2>&1
        """


rule classify_hitac_standalone:
    input:
        query = "data/test/{dataset}.fasta",
        classifier = "results/temp/{dataset}/{penalty}/hitac_standalone/classifier.pkl"
    output:
        predictions = "results/predictions/{dataset}/{penalty}hitac_standalone.tsv"
    benchmark:
        repeat("results/benchmark/{dataset}/{penalty}/classify/hitac_standalone.tsv",config["benchmark"]["repeat"])
    threads:
        config["threads"]
    log:
        "results/logs/{dataset}_{penalty}_classify_hitac_standalone.txt"
    conda:
        "../envs/hitac_tuning.yml"
    shell:
        """
        hitac-classify \
            --reads {input.query} \
            --classifier {input.classifier} \
            --kmer 6 \
            --threads {threads} \
            --classification {output.predictions} \
            > {log} 2>&1
        """
