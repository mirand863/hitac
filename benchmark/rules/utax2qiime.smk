rule utax2qiime:
    input:
        train = "data/train/{dataset}.fasta",
        test = "data/test/{dataset}.fasta",
        scripts = expand("scripts/{script}",script=config["scripts"])
    output:
        dbq = temp("results/temp/{dataset}/utax2qiime/dbq.fa"),
        dbtax = temp("results/temp/{dataset}/utax2qiime/db-tax.txt")
    container:
        "docker://python:2.7-slim"
    shell:
        """
        python scripts/fasta_utax2qiime.py \
            {input.train} \
            {output.dbq} \
            {output.dbtax}
        """
