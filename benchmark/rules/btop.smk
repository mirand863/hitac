rule taxxi2btop:
    input:
        train = "data/train/{dataset}.fasta"
    output:
        reference = temp("results/temp/{dataset}/btop/reference.fasta")
    shell:
        """
        sed \
            "-es/;.*//" \
            < {input.train} \
            > {output.reference}
        """


rule btop:
    input:
        reference = "results/temp/{dataset}/btop/reference.fasta",
        test = "data/test/{dataset}.fasta"
    output:
        ndb = temp("results/temp/{dataset}/btop/database.ndb"),
        nhr = temp("results/temp/{dataset}/btop/database.nhr"),
        nin = temp("results/temp/{dataset}/btop/database.nin"),
        nog = temp("results/temp/{dataset}/btop/database.nog"),
        nos = temp("results/temp/{dataset}/btop/database.nos"),
        not_ = temp("results/temp/{dataset}/btop/database.not"),
        nsq = temp("results/temp/{dataset}/btop/database.nsq"),
        ntf = temp("results/temp/{dataset}/btop/database.ntf"),
        nto = temp("results/temp/{dataset}/btop/database.nto"),
        predictions = temp("results/temp/{dataset}/btop/predictions.tsv")
    params:
        database = "results/temp/{dataset}/btop/database"
    # benchmark:
    #     repeat("results/benchmark/{dataset}/btop.tsv", config["benchmark"]["repeat"])
    threads:
        config["threads"]
    container:
        config["containers"]["btop"]
    shell:
        """
        makeblastdb \
            -in {input.reference} \
            -dbtype nucl \
            -parse_seqids \
            -out {params.database}
        
        blastn \
            -task megablast \
            -db {params.database} \
            -query {input.test} \
            -num_threads {threads} \
            -max_target_seqs 1 \
            -outfmt "6 qseqid sseqid" \
            -evalue 0.01 \
            > {output.predictions}
        """


rule btop2tab:
    input:
        predictions = "results/temp/{dataset}/btop/predictions.tsv",
        train = "data/train/{dataset}.fasta",
        scripts = expand("scripts/{script}", script=config["scripts"])
    output:
        predictions = "results/predictions/{dataset}/btop.tsv"
    container:
        "docker://python:3.6-slim"
    shell:
        """
        python scripts/btop2tab.py \
            {input.predictions} \
            {input.train} \
            {output.predictions}
        """
