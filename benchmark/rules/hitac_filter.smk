rule hitac_filter_fit:
    input:
        reference_reads = "results/temp/{dataset}/qiime2/reference_reads.qza",
        reference_taxonomy = "results/temp/{dataset}/qiime2/reference_taxonomy.qza"
    output:
        filter = temp("results/temp/{dataset}/hitac_filter/filter.qza")
    benchmark:
        repeat("results/benchmark/{dataset}/hitac_filter_fit.tsv", config["benchmark"]["repeat"])
    threads:
        config["threads"]
    container:
        config["containers"]["hitac"]
    shell:
        """
        qiime hitac fit-filter \
            --i-reference-reads {input.reference_reads} \
            --i-reference-taxonomy {input.reference_taxonomy} \
            --p-kmer 6 \
            --p-threads {threads} \
            --o-filter {output.filter}
        """


rule hitac_filter_predict:
    input:
        filter = "results/temp/{dataset}/hitac_filter/filter.qza",
        query_reads = "results/temp/{dataset}/qiime2/query_reads.qza",
        unfiltered_predictions = "results/temp/{dataset}/hitac/predictions.qza"
    output:
        filtered_predictions = temp("results/temp/{dataset}/hitac_filter/predictions.qza")
    benchmark:
        repeat("results/benchmark/{dataset}/hitac_filter_predict.tsv", config["benchmark"]["repeat"])
    threads:
        config["threads"]
    container:
        config["containers"]["hitac"]
    shell:
        """
        qiime hitac filter \
            --i-filter {input.filter} \
            --i-reads {input.query_reads} \
            --i-classification {input.unfiltered_predictions} \
            --p-threshold 0.7 \
            --p-kmer 6 \
            --p-threads {threads} \
            --o-filtered-classification {output.filtered_predictions}
        """
