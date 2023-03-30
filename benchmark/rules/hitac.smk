rule hitac_fit:
    input:
        reference_reads = "results/temp/{dataset}/qiime2/reference_reads.qza",
        reference_taxonomy = "results/temp/{dataset}/qiime2/reference_taxonomy.qza"
    output:
        classifier = temp("results/temp/{dataset}/hitac/classifier.qza"),
    benchmark:
        repeat("results/benchmark/{dataset}/hitac_fit.tsv", config["benchmark"]["repeat"])
    threads:
        config["threads"]
    container:
        config["containers"]["hitac"]
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
        query_reads = "results/temp/{dataset}/qiime2/query_reads.qza",
        classifier = "results/temp/{dataset}/hitac/classifier.qza",
    output:
        predictions = temp("results/temp/{dataset}/hitac/predictions.qza"),
    benchmark:
        repeat("results/benchmark/{dataset}/hitac_predict.tsv", config["benchmark"]["repeat"])
    threads:
        config["threads"]
    container:
        config["containers"]["hitac"]
    shell:
        """
        qiime hitac classify \
            --i-reads {input.query_reads} \
            --i-classifier {input.classifier} \
            --p-kmer 6 \
            --p-threads {threads} \
            --o-classification {output.predictions}
        """
