rule hitac_fit:
    input:
        reference_reads = "results/temp/{dataset}/qiime_import/reference_reads.qza",
        reference_taxonomy = "results/temp/{dataset}/qiime_import/reference_taxonomy.qza"
    output:
        classifier = temp("results/temp/{dataset}/hitac/classifier.qza"),
    # benchmark:
        # repeat("results/benchmark/{dataset}/hitac_fit.tsv", config["benchmark"]["repeat"])
    threads:
        config["threads"]
    container:
        "docker://mirand863/hitac:2.0.29-beta.6"
    shell:
        """
        qiime hitac fit \
            --i-reference-reads {input.reference_reads} \
            --i-reference-taxonomy {input.reference_taxonomy} \
            --p-kmer 6 \
            --p-threads {threads} \
            --o-classifier {output.classifier}
        """


rule hitac_predict:
    input:
        query_reads = "results/temp/{dataset}/qiime_import/query_reads.qza",
        classifier = "results/temp/{dataset}/hitac/classifier.qza",
    output:
        predictions = temp("results/temp/{dataset}/hitac/predictions.qza"),
    # benchmark:
        # repeat("results/benchmark/{dataset}/hitac_predict.tsv", config["benchmark"]["repeat"])
    threads:
        config["threads"]
    container:
        "docker://mirand863/hitac:2.0.29-beta.6"
    shell:
        """
        qiime hitac classify \
            --i-reads {input.query_reads} \
            --i-classifier {input.classifier} \
            --p-kmer 6 \
            --p-threads {threads} \
            --o-classification {output.predictions}
        """


rule qiime_export:
    input:
        predictions = "results/temp/{dataset}/hitac/predictions.qza"
    output:
        taxonomy = temp("results/temp/{dataset}/hitac/taxonomy.tsv")
    params:
        output_dir = "results/temp/{dataset}/hitac"
    container:
        "docker://quay.io/qiime2/core:2023.2"
    shell:
        """
        qiime tools export \
            --input-path {input.predictions} \
            --output-path {params.output_dir}
        """


rule qiime2tax2tab:
    input:
        taxonomy = "results/temp/{dataset}/hitac/taxonomy.tsv"
    output:
        predictions = "results/predictions/{dataset}/hitac.tsv"
    container:
        "docker://python:2.7-slim"
    shell:
        """
        python scripts/qiime2tax2tab.py \
            {input.taxonomy} \
            > {output.predictions}
        """
