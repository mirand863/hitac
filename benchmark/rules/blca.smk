rule taxxi2blca:
    input:
        train = "data/train/{dataset}.fasta",
        test = "data/test/{dataset}.fasta",
        scripts = expand("scripts/{script}",script=config["scripts"])
    output:
        reference_reads = temp("results/temp/{dataset}/blca/reference_reads.fasta"),
        reference_taxonomy = temp("results/temp/{dataset}/blca/reference_taxonomy.txt"),
        query_reads = temp("results/temp/{dataset}/blca/query_reads.fasta"),
        query_taxonomy = temp("results/temp/{dataset}/blca/query_taxonomy.txt")
    container:
        config["containers"]["blca"]
    shell:
        """
        python scripts/fasta_utax2_to_blca.py \
            {input.train} \
            {output.reference_reads} \
            {output.reference_taxonomy}

        python scripts/fasta_utax2_to_blca.py \
            {input.test} \
            {output.query_reads} \
            {output.query_taxonomy}
        """


rule train_blca:
    input:
        reference_reads = "results/temp/{dataset}/blca/reference_reads.fasta"
    output:
        ndb = temp("results/temp/{dataset}/blca/database.ndb"),
        nhr = temp("results/temp/{dataset}/blca/database.nhr"),
        nin = temp("results/temp/{dataset}/blca/database.nin"),
        nog = temp("results/temp/{dataset}/blca/database.nog"),
        nos = temp("results/temp/{dataset}/blca/database.nos"),
        not_ = temp("results/temp/{dataset}/blca/database.not"),
        nsq = temp("results/temp/{dataset}/blca/database.nsq"),
        ntf = temp("results/temp/{dataset}/blca/database.ntf"),
        nto = temp("results/temp/{dataset}/blca/database.nto")
    params:
        database = "results/temp/{dataset}/blca/database"
    benchmark:
        repeat("results/benchmark/{dataset}/train/blca.tsv", config["benchmark"]["repeat"])
    threads:
        config["threads"]
    container:
        config["containers"]["blca"]
    shell:
        """
        makeblastdb \
            -in {input.reference_reads} \
            -dbtype nucl \
            -parse_seqids \
            -out {params.database}
        """


rule classify_blca:
    input:
        ndb = "results/temp/{dataset}/blca/database.ndb",
        nhr = "results/temp/{dataset}/blca/database.nhr",
        nin = "results/temp/{dataset}/blca/database.nin",
        nog = "results/temp/{dataset}/blca/database.nog",
        nos = "results/temp/{dataset}/blca/database.nos",
        not_ = "results/temp/{dataset}/blca/database.not",
        nsq = "results/temp/{dataset}/blca/database.nsq",
        ntf = "results/temp/{dataset}/blca/database.ntf",
        nto = "results/temp/{dataset}/blca/database.nto",
        query_reads = "results/temp/{dataset}/blca/query_reads.fasta",
        reference_taxonomy = "results/temp/{dataset}/blca/reference_taxonomy.txt"
    output:
        predictions = temp("results/temp/{dataset}/blca/query_reads.fasta.blca.out")
    params:
        database = "results/temp/{dataset}/blca/database"
    benchmark:
        repeat("results/benchmark/{dataset}/classify/blca.tsv", config["benchmark"]["repeat"])
    threads:
        config["threads"]
    container:
        config["containers"]["blca"]
    shell:
        """
        2.blca_main.py \
            -i {input.query_reads} \
            -r {input.reference_taxonomy} \
            -q {params.database} \
            --proc {threads}
        """


rule blca2taxxi:
    input:
        predictions = "results/temp/{dataset}/blca/query_reads.fasta.blca.out",
        test = "data/test/{dataset}.fasta",
    output:
        predictions = "results/predictions/{dataset}/blca.tsv"
    container:
        config["containers"]["blca"]
    shell:
        """
        python scripts/blca2tab.py \
            {input.predictions} \
            {input.test} \
            > {output.predictions}
        """
