rule classify_microclass:
    input:
        train = "data/train/{dataset}.fasta",
        test = "data/test/{dataset}.fasta",
        scripts = expand("scripts/{script}",script=config["scripts"])
    output:
        predictions = temp("results/temp/{dataset}/microclass/predictions.tsv")
    benchmark:
        repeat("results/benchmark/{dataset}/classify/microclass.tsv", config["benchmark"]["repeat"])
    threads:
        config["threads"]
    container:
        config["containers"]["microclass"]
    shell:
        """
        Rscript scripts/microclass.R \
            {input.train} \
            {input.test} \
            {output.predictions}
        """


rule microclass2taxxi:
    input:
        predictions = "results/temp/{dataset}/microclass/predictions.tsv",
        scripts = expand("scripts/{script}",script=config["scripts"])
    output:
        predictions = "results/predictions/{dataset}/microclass.tsv"
    container:
        config["containers"]["pandas"]
    shell:
        """
        python scripts/microclass2tab.py \
            {input.predictions} \
            {output.predictions}
        """
