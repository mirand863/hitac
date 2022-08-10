rule top:
    input:
        train = "data/train/{dataset}.fasta",
        test = "data/test/{dataset}.fasta",
        usearch = "bin/usearch"
    output:
        predictions = "results/predictions/{dataset}/top.tsv"
    benchmark:
        repeat("results/benchmark/{dataset}/top.tsv", config["benchmark"]["repeat"])
    threads:
        config["threads"]
    shell:
        """
        {input.usearch} \
            -db {input.train} \
            -cons_tax {input.test} \
            -strand plus \
            -tabbedout {output.predictions} \
            -strand plus \
            -id 0.7 \
            -maxaccepts 3 \
            -maxrejects 16 \
            -top_hit_only
        """
