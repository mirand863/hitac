rule microclass:
    input:
        train = "data/train/{dataset}.fasta",
        test = "data/test/{dataset}.fasta"
    output:
        predictions = temp("results/temp/{dataset}/microclass/predictions.tsv")
    benchmark:
        repeat("results/benchmark/{dataset}/microclass.tsv", config["benchmark"]["repeat"])
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
        predictions = "results/temp/{dataset}/microclass/predictions.tsv"
    output:
        predictions = "results/predictions/{dataset}/microclass.tsv"
    container:
        config["containers"]["python2"]
    shell:
        """
        python scripts/microclass2tab.py \
            {input.predictions} \
            {output.predictions}
        """
