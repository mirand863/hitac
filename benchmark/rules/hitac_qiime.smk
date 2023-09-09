rule hitac_qiime:
    input:
        reference_reads = "results/temp/{dataset}/qiime2/reference_reads.qza",
        reference_taxonomy = "results/temp/{dataset}/qiime2/reference_taxonomy.qza",
        query_reads = "results/temp/{dataset}/qiime2/query_reads.qza"
    output:
        classifier = temp("results/temp/{dataset}/hitac_qiime/classifier.qza"),
        predictions = temp("results/temp/{dataset}/hitac_qiime/predictions.qza")
    benchmark:
        repeat("results/benchmark/{dataset}/hitac_qiime.tsv", config["benchmark"]["repeat"])
    threads:
        config["threads"]
    container:
        config["containers"]["hitac_qiime"]
    shell:
        """
        qiime hitac fit \
            --i-reference-reads {input.reference_reads} \
            --i-reference-taxonomy {input.reference_taxonomy} \
            --p-kmer 6 \
            --p-threads {threads} \
            --o-classifier {output.classifier}

        qiime hitac classify \
            --i-reads {input.query_reads} \
            --i-classifier {output.classifier} \
            --p-kmer 6 \
            --p-threads {threads} \
            --o-classification {output.predictions}
        """