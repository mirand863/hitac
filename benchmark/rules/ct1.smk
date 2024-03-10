rule classify_ct1:
    input:
        train = "data/train/{dataset}.fasta",
        test = "data/test/{dataset}.fasta",
    output:
        predictions = "results/predictions/{dataset}/ct1.tsv"
    benchmark:
        repeat("results/benchmark/{dataset}/classify/ct1.tsv", config["benchmark"]["repeat"])
    threads:
        config["threads"]
    container:
        config["containers"]["usearch"]
    shell:
        """
        usearch \
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
