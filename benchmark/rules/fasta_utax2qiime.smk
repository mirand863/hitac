rule fasta_utax2qiime:
    input:
        train = "data/train/{dataset}.fasta",
        scripts = expand("scripts/{script}",script=config["scripts"])
    output:
        sequences = "results/temp/{dataset}/dbq.fa",
        taxonomy = "results/temp/{dataset}/db-tax.txt"
    conda:
        "../envs/python2.yml"
    shell:
        """
        python2 scripts/fasta_utax2qiime.py \
            {input.train} \
            {output.sequences} \
            {output.taxonomy}
        """
