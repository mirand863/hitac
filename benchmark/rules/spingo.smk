rule taxxi2spingo:
    input:
        train = "data/train/{dataset}.fasta",
        scripts = expand("scripts/{script}",script=config["scripts"])
    output:
        reference_reads = temp("results/temp/{dataset}/spingo/reference_reads.fasta")
    container:
        config["containers"]["python2"]
    shell:
        """
        python scripts/fasta_utax2spingo.py \
            {input.train} \
            > {output.reference_reads}
        """


rule spingo:
    input:
        reference_reads = "results/temp/{dataset}/spingo/reference_reads.fasta",
        test = "data/test/{dataset}.fasta"
    output:
        predictions = temp("results/temp/{dataset}/spingo/predictions.tsv")
    benchmark:
        repeat("results/benchmark/{dataset}/spingo.tsv",config["benchmark"]["repeat"])
    threads:
        config["threads"]
    container:
        config["containers"]["spingo"]
    shell:
        """
        spingo \
            -i {input.test} \
            -d {input.reference_reads} \
            -p {threads} \
            > {output.predictions}
        """


rule spingo2taxxi:
    input:
        predictions = "results/temp/{dataset}/spingo/predictions.tsv"
    output:
        predictions = "results/predictions/{dataset}/spingo.tsv"
    container:
        config["containers"]["python2"]
    shell:
        """
        python scripts/spingo2tab.py \
            {input.predictions} \
            > {output.predictions}
        """
