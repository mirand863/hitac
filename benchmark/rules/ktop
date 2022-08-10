rule ktop:
    input:
        train = "data/train/{dataset}.fasta",
        test = "data/test/{dataset}.fasta",
        usearch = "bin/usearch"
    output:
        predictions = "results/predictions/{dataset}/ktop.tsv"
    benchmark:
        repeat("results/benchmark/{dataset}/ktop.tsv", config["benchmark"]["repeat"])
    threads:
        config["threads"]
    shell:
        """
        {input.usearch} \
            -db {input.train} \
            -sintax {input.test} \
            -strand plus \
            -tabbedout \
            {output.predictions} \
            -strand plus \
            -ktop
        """
