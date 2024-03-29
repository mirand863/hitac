rule taxxi2btop:
    input:
        train = "data/train/{dataset}.fasta"
    output:
        reference = temp("results/temp/{dataset}/btop/reference.fasta")
    container:
        config["containers"]["btop"]
    shell:
        """
        sed \
            "-es/;.*//" \
            < {input.train} \
            > {output.reference}
        """


rule train_btop:
    input:
        reference = "results/temp/{dataset}/btop/reference.fasta"
    output:
        ndb = temp("results/temp/{dataset}/btop/database.ndb"),
        nhr = temp("results/temp/{dataset}/btop/database.nhr"),
        nin = temp("results/temp/{dataset}/btop/database.nin"),
        nog = temp("results/temp/{dataset}/btop/database.nog"),
        nos = temp("results/temp/{dataset}/btop/database.nos"),
        not_ = temp("results/temp/{dataset}/btop/database.not"),
        nsq = temp("results/temp/{dataset}/btop/database.nsq"),
        ntf = temp("results/temp/{dataset}/btop/database.ntf"),
        nto = temp("results/temp/{dataset}/btop/database.nto")
    params:
        database="results/temp/{dataset}/btop/database"
    benchmark:
        repeat("results/benchmark/{dataset}/train/btop.tsv",config["benchmark"]["repeat"])
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
        """


rule classify_btop:
    input:
        ndb = "results/temp/{dataset}/btop/database.ndb",
        nhr = "results/temp/{dataset}/btop/database.nhr",
        nin = "results/temp/{dataset}/btop/database.nin",
        nog = "results/temp/{dataset}/btop/database.nog",
        nos = "results/temp/{dataset}/btop/database.nos",
        not_ = "results/temp/{dataset}/btop/database.not",
        nsq = "results/temp/{dataset}/btop/database.nsq",
        ntf = "results/temp/{dataset}/btop/database.ntf",
        nto = "results/temp/{dataset}/btop/database.nto",
        test = "data/test/{dataset}.fasta"
    output:
        predictions = temp("results/temp/{dataset}/btop/predictions.tsv")
    params:
        database = "results/temp/{dataset}/btop/database"
    benchmark:
        repeat("results/benchmark/{dataset}/classify/btop.tsv", config["benchmark"]["repeat"])
    threads:
        config["threads"]
    container:
        config["containers"]["btop"]
    shell:
        """
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


rule btop2taxxi:
    input:
        predictions = "results/temp/{dataset}/btop/predictions.tsv",
        train = "data/train/{dataset}.fasta",
        scripts = expand("scripts/{script}", script=config["scripts"])
    output:
        predictions = "results/predictions/{dataset}/btop.tsv"
    container:
        config["containers"]["btop"]
    shell:
        """
        python scripts/btop2tab.py \
            {input.predictions} \
            {input.train} \
            {output.predictions}
        """
