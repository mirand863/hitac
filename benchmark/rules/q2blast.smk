rule classify_q2blast:
    input:
        reference_reads = "results/temp/{dataset}/qiime2/reference_reads.qza",
        reference_taxonomy = "results/temp/{dataset}/qiime2/reference_taxonomy.qza",
        query_reads = "results/temp/{dataset}/qiime2/query_reads.qza"
    output:
        predictions = temp("results/temp/{dataset}/q2blast/predictions.qza"),
        search_results = temp("results/temp/{dataset}/q2blast/search_results.qza")
    benchmark:
        repeat("results/benchmark/{dataset}/classify/q2blast.tsv", config["benchmark"]["repeat"])
    threads:
        config["threads"]
    container:
        config["containers"]["qiime2"]
    shell:
        """
        qiime feature-classifier classify-consensus-blast \
            --i-query {input.query_reads} \
            --i-reference-reads {input.reference_reads} \
            --i-reference-taxonomy {input.reference_taxonomy} \
            --o-classification {output.predictions} \
            --o-search-results {output.search_results}
        """
