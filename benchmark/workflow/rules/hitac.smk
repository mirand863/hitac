rule hitac:
    input:
        reference_features = "results/hitac/features/train/{dataset}/feat_extraction/DNC.csv",
        reference_taxonomy = "results/temp/{dataset}/qiime2/reference_taxonomy.qza",
        query_reads = "results/temp/{dataset}/qiime2/query_reads.qza"
    output:
        classifier = temp("results/temp/{dataset}/hitac/classifier.qza"),
        predictions = temp("results/temp/{dataset}/hitac/predictions.qza")
    benchmark:
        repeat("results/benchmark/{dataset}/hitac.tsv", config["benchmark"]["repeat"])
    params:
        reference_features_dir = "results/hitac/features/train/{dataset}/feat_extraction"
    threads:
        config["threads"]
    container:
        config["containers"]["hitac"]
    shell:
        """
        qiime hitac fit \
            --p-features-dir {params.reference_features_dir} \
            --i-reference-taxonomy {input.reference_taxonomy} \
            --p-threads {threads} \
            --o-classifier {output.classifier}
            --verbose

        # qiime hitac classify \
        #     --i-reads {input.query_reads} \
        #     --i-classifier {output.classifier} \
        #     --p-kmer 6 \
        #     --p-threads {threads} \
        #     --o-classification {output.predictions}
        #     --verbose
        """
