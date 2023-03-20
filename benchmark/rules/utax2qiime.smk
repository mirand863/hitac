rule utax2qiime:
    input:
        train = "data/train/{dataset}.fasta",
        scripts = expand("scripts/{script}",script=config["scripts"])
    output:
        reference_reads = temp("results/temp/{dataset}/utax2qiime/reference_reads.fasta"),
        reference_taxonomy = temp("results/temp/{dataset}/utax2qiime/reference_taxonomy.txt")
    container:
        "docker://python:2.7-slim"
    shell:
        """
        python scripts/fasta_utax2qiime.py \
            {input.train} \
            {output.reference_reads} \
            {output.reference_taxonomy}
        """
