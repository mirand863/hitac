rule train_hitac_uncertainty:
    input:
        reference = "data/train/{dataset}.fasta"
    output:
        classifier = "results/temp/{dataset}/hitac_uncertainty/{calibration_method}/{calibration_percentage}/classifier.pkl"
    params:
        calibration_percentage = 15
    benchmark:
        repeat("results/benchmark/{dataset}/train/{calibration_method}/{calibration_percentage}/hitac_uncertainty.tsv",config["benchmark"]["repeat"])
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
            --calibration-percentage {params.calibration_percentage} \
            --classifier {output.classifier}
        """


# rule predict_hitac_uncertainty:
#     input:
#         query = "data/test/{dataset}.fasta",
#         classifier = "results/temp/{dataset}/hitac_uncertainty/{calibration_method}/classifier.pkl"
#     output:
#         predictions = "results/predictions/{dataset}/{calibration_method}/hitac_uncertainty.tsv"
#     benchmark:
#         repeat("results/benchmark/{dataset}/predict/{calibration_method}/hitac_uncertainty.tsv",config["benchmark"]["repeat"])
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


# rule probability_hitac_uncertainty:
#     input:
#         query = "data/test/{dataset}.fasta",
#         classifier = "results/temp/{dataset}/hitac_uncertainty/{calibration_method}/classifier.pkl"
#     output:
#         predictions = "results/predictions/{dataset}/{calibration_method}/hitac_uncertainty.tsv"
#     benchmark:
#         repeat("results/benchmark/{dataset}/predict/{calibration_method}/hitac_uncertainty.tsv",config["benchmark"]["repeat"])
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
