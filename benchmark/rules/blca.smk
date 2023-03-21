rule utax2blca:
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
        "docker://python:2.7-slim"
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


rule blca:
    input:
        reference_reads = "results/temp/{dataset}/blca/reference_reads.fasta",
        query_reads = "results/temp/{dataset}/blca/query_reads.fasta",
        reference_taxonomy = "results/temp/{dataset}/blca/reference_taxonomy.txt",
    output:
        ndb = temp("results/temp/{dataset}/blca/database.ndb"),
        nhr = temp("results/temp/{dataset}/blca/database.nhr"),
        nin = temp("results/temp/{dataset}/blca/database.nin"),
        nog = temp("results/temp/{dataset}/blca/database.nog"),
        nos = temp("results/temp/{dataset}/blca/database.nos"),
        not_ = temp("results/temp/{dataset}/blca/database.not"),
        nsq = temp("results/temp/{dataset}/blca/database.nsq"),
        ntf = temp("results/temp/{dataset}/blca/database.ntf"),
        nto = temp("results/temp/{dataset}/blca/database.nto"),
        predictions = temp("results/temp/{dataset}/blca/query_reads.fasta.blca.out")
    params:
        database = "results/temp/{dataset}/blca/database"
    # benchmark:
    #     repeat("results/benchmark/{dataset}/blca.tsv", config["benchmark"]["repeat"])
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
            
        python /BLCA-2.3-alpha/2.blca_main.py \
            -i {input.query_reads} \
            -r {input.reference_taxonomy} \
            -q {params.database} \
            --proc {threads}
        """


# rule blca2tab:
#     input:
#         query_reads = "results/temp/{dataset}/blca/query_reads.fasta",
#         reference_taxonomy = "results/temp/{dataset}/blca/reference_taxonomy.txt"
#     output:
#         predictions = "results/predictions/{dataset}/blca.tsv",
#         tmpdir= temp(directory("results/temp/{dataset}/blca"))
#     params:
#         database = "results/temp/{dataset}/blca/database"
#     benchmark:
#         repeat("results/benchmark/{dataset}/blca.tsv", config["benchmark"]["repeat"])
#     threads:
#         config["threads"]
#     conda:
#         "../envs/blca.yml"
#     shell:
#         """
#         python blca \
#             -i {input.query_reads} \
#             -r {input.reference_taxonomy} \
#             -q {params.database} \
#             --proc {threads}
#
#         python scripts/blca2tab.py \
#             {output.tmpdir}/q.fa.blca.out \
#             {input.test} \
#             > {output.predictions}
#         """
