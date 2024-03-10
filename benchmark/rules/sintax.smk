rule classify_sintax:
    input:
        train = "data/train/{dataset}.fasta",
        test = "data/test/{dataset}.fasta"
    output:
        predictions = temp("results/temp/{dataset}/sintax/predictions.tsv")
    benchmark:
        repeat("results/benchmark/{dataset}/classify/sintax.tsv", config["benchmark"]["repeat"])
    threads:
        config["threads"]
    container:
        config["containers"]["usearch"]
    shell:
        """
        usearch \
            -sintax \
            {input.test} \
            -db {input.train} \
            -strand plus \
            -tabbedout {output.predictions}
        """


rule sintax50:
    input:
        predictions = "results/temp/{dataset}/sintax/predictions.tsv",
        scripts = expand("scripts/{script}",script=config["scripts"])
    output:
        predictions = "results/predictions/{dataset}/sintax50.tsv",
    container:
        config["containers"]["python2"]
    shell:
        """
        python scripts/bbc_cutoff.py \
            {input.predictions} \
            0.5 \
            > {output.predictions}
        """


rule sintax80:
    input:
        predictions = "results/temp/{dataset}/sintax/predictions.tsv",
        scripts = expand("scripts/{script}",script=config["scripts"])
    output:
        predictions = "results/predictions/{dataset}/sintax80.tsv"
    container:
        config["containers"]["python2"]
    shell:
        """
        python scripts/bbc_cutoff.py \
            {input.predictions} \
            0.8 \
            > {output.predictions}
        """
