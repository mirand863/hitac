rule ct1:
    input:
        train = "data/train/{dataset}.fasta",
        test = "data/test/{dataset}.fasta",
        usearch = "bin/usearch"
    output:
        predictions = "results/predictions/{dataset}/ct1.tsv"
    benchmark:
        repeat("results/benchmark/{dataset}/ct1.tsv", config["benchmark"]["repeat"])
    threads:
        config["threads"]
    shell:
        """
        {input.usearch} \
            -db {input.train} \
            -cons_tax {input.test} \
            -strand plus \
            -tabbedout \
            {output.predictions} \
            -strand plus \
            -id 0.7 \
            -maxaccepts 3 \
            -maxrejects 8 \
            -maj 0.51
        """
