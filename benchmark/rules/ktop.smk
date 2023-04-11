rule ktop:
    input:
        train = "data/train/{dataset}.fasta",
        test = "data/test/{dataset}.fasta"
    output:
        predictions = "results/predictions/{dataset}/ktop.tsv"
    benchmark:
        repeat("results/benchmark/{dataset}/ktop.tsv", config["benchmark"]["repeat"])
    threads:
        config["threads"]
    container:
        config["containers"]["usearch"]
    shell:
        """
        usearch \
            -db {input.train} \
            -sintax {input.test} \
            -strand plus \
            -tabbedout \
            {output.predictions} \
            -strand plus \
            -ktop
        """
