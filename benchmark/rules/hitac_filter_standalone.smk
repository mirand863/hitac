rule hitac_filter_standalone:
    input:
        reference = "data/train/{dataset}.fasta",
        query = "data/test/{dataset}.fasta",
        unfiltered_predictions = "results/predictions/{dataset}/hitac_standalone.tsv"
    output:
        filter = temp("results/temp/{dataset}/hitac_filter_standalone/classifier.pkl"),
        filtered_predictions = temp("results/predictions/{dataset}/hitac_filter_standalone.tsv")
    benchmark:
        repeat("results/benchmark/{dataset}/hitac_standalone.tsv",config["benchmark"]["repeat"])
    threads:
        config["threads"]
    container:
        config["containers"]["hitac_standalone"]
    shell:
        """
        hitac-fit-filter \
            --reference {input.reference} \
            --kmer 6 \
            --threads {threads} \
            --filter {output.filter}

        hitac-filter \
            --filter {output.filter} \
            --reads {input.query} \
            --classification {input.unfiltered_predictions} \
            --threshold 0.7 \
            --kmer 6 \
            --threads {threads} \
            --filtered-classification {output.filtered_predictions}
        """
