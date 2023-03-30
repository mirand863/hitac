rule q2vs:
    input:
        query_reads = "results/temp/{dataset}/qiime2/query_reads.qza",
        reference_reads = "results/temp/{dataset}/qiime2/reference_reads.qza",
        reference_taxonomy = "results/temp/{dataset}/qiime2/reference_taxonomy.qza"
    output:
        predictions = temp("results/temp/{dataset}/q2vs/predictions.qza"),
        search_results = temp("results/temp/{dataset}/q2vs/search_results.qza")
    benchmark:
        repeat("results/benchmark/{dataset}/q2vs.tsv", config["benchmark"]["repeat"])
    threads:
        config["threads"]
    container:
        config["containers"]["qiime2"]
    shell:
        """
        qiime feature-classifier classify-consensus-vsearch \
            --i-query {input.query_reads} \
            --p-threads {threads} \
            --i-reference-reads {input.reference_reads} \
            --i-reference-taxonomy {input.reference_taxonomy} \
            --o-classification {output.predictions} \
            --o-search-results {output.search_results}
        """
