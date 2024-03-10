rule train_q2sk:
    input:
        reference_reads = "results/temp/{dataset}/qiime2/reference_reads.qza",
        reference_taxonomy = "results/temp/{dataset}/qiime2/reference_taxonomy.qza"
    output:
        classifier = temp("results/temp/{dataset}/q2sk/classifier.qza")
    benchmark:
        repeat("results/benchmark/{dataset}/train/q2sk.tsv", config["benchmark"]["repeat"])
    threads:
        config["threads"]
    container:
        config["containers"]["qiime2"]
    shell:
        """
        qiime feature-classifier fit-classifier-naive-bayes \
            --i-reference-reads {input.reference_reads} \
            --i-reference-taxonomy {input.reference_taxonomy} \
            --o-classifier {output.classifier}
        """


rule classify_q2sk:
    input:
        query_reads = "results/temp/{dataset}/qiime2/query_reads.qza",
        classifier = "results/temp/{dataset}/q2sk/classifier.qza"
    output:
        predictions = temp("results/temp/{dataset}/q2sk/predictions.qza")
    benchmark:
        repeat("results/benchmark/{dataset}/classify/q2sk.tsv", config["benchmark"]["repeat"])
    threads:
        config["threads"]
    container:
        config["containers"]["qiime2"]
    shell:
        """
        qiime feature-classifier classify-sklearn \
            --i-classifier {input.classifier} \
            --i-reads {input.query_reads} \
            --p-n-jobs {threads} \
            --o-classification {output.predictions}
        """
