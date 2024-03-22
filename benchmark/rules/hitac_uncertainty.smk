rule train_hitac_uncertainty:
    input:
        reference = "data/train/{dataset}.fasta"
    output:
        classifier = "results/temp/{dataset}/hitac_uncertainty/{calibration_method}/classifier.pkl"
    benchmark:
        repeat("results/benchmark/{dataset}/train/{calibration_method}/hitac_uncertainty.tsv",config["benchmark"]["repeat"])
    threads:
        config["threads"]
    conda:
        "../envs/hitac_uncertainty.yml"
    shell:
        """
        hitac-fit \
            --reference {input.reference} \
            --kmer 6 \
            --threads {threads} \
            --calibration-method {wildcards.calibration_method} \
            --classifier {output.classifier}
        """


# rule classify_hitac_uncertainty:
#     input:
#         query = "data/test/{dataset}.fasta",
#         classifier = "results/temp/{dataset}/hitac_standalone/classifier.pkl"
#     output:
#         predictions = "results/predictions/{dataset}/hitac_standalone.tsv"
#     benchmark:
#         repeat("results/benchmark/{dataset}/classify/hitac_standalone.tsv",config["benchmark"]["repeat"])
#     threads:
#         config["threads"]
#     conda:
#         "../envs/hitac_uncertainty.yml"
#     shell:
#         """
#         hitac-classify \
#             --reads {input.query} \
#             --classifier {input.classifier} \
#             --kmer 6 \
#             --threads {threads} \
#             --classification {output.predictions}
#         """
