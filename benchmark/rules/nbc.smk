rule classify_nbc:
    input:
        train = "data/train/{dataset}.fasta",
        test = "data/test/{dataset}.fasta"
    output:
        predictions = temp("results/temp/{dataset}/nbc/predictions.tsv")
    benchmark:
        repeat("results/benchmark/{dataset}/classify/nbc.tsv", config["benchmark"]["repeat"])
    threads:
        config["threads"]
    container:
        config["containers"]["usearch"]
    shell:
        """
        usearch \
            -nbc_tax \
            {input.test} \
            -db {input.train} \
            -strand plus \
            -tabbedout {output.predictions}
        """


rule nbc50:
    input:
        predictions = "results/temp/{dataset}/nbc/predictions.tsv",
        scripts = expand("scripts/{script}",script=config["scripts"])
    output:
        predictions = "results/predictions/{dataset}/nbc50.tsv"
    container:
        config["containers"]["python2"]
    shell:
        """
        python scripts/bbc_cutoff.py \
            {input.predictions} \
            0.5 \
            > {output.predictions}
        """


rule nbc80:
    input:
        predictions = "results/temp/{dataset}/nbc/predictions.tsv",
        scripts = expand("scripts/{script}",script=config["scripts"])
    output:
        predictions = "results/predictions/{dataset}/nbc80.tsv"
    container:
        config["containers"]["python2"]
    shell:
        """
        python scripts/bbc_cutoff.py \
            {input.predictions} \
            0.8 \
            > {output.predictions}
        """
