rule hitac_filter:
    input:
        reference_reads = "results/temp/{dataset}/qiime2/reference_reads.qza",
        reference_taxonomy = "results/temp/{dataset}/qiime2/reference_taxonomy.qza",
        query_reads = "results/temp/{dataset}/qiime2/query_reads.qza",
        unfiltered_predictions = "results/temp/{dataset}/hitac/predictions.qza"
    output:
        filter = temp("results/temp/{dataset}/hitac_filter/filter.qza"),
        filtered_predictions = temp("results/temp/{dataset}/hitac_filter/predictions.qza")
    benchmark:
        repeat("results/benchmark/{dataset}/hitac_filter.tsv", config["benchmark"]["repeat"])
    threads:
        config["threads"]
    container:
        config["containers"]["hitac_qiime"]
    shell:
        """
        qiime hitac fit-filter \
            --i-reference-reads {input.reference_reads} \
            --i-reference-taxonomy {input.reference_taxonomy} \
            --p-kmer 6 \
            --p-threads {threads} \
            --o-filter {output.filter}

        qiime hitac filter \
            --i-filter {output.filter} \
            --i-reads {input.query_reads} \
            --i-classification {input.unfiltered_predictions} \
            --p-threshold 0.7 \
            --p-kmer 6 \
            --p-threads {threads} \
            --o-filtered-classification {output.filtered_predictions}
        """
