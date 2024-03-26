rule train_hitac_uncertainty:
    input:
        reference = "data/train/{dataset}.fasta"
    output:
        classifier = "results/temp/{dataset}/hitac_uncertainty/{calibration_method}/{calibration_percentage}/classifier.pkl"
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
            --calibration-percentage {wildcards.calibration_percentage} \
            --classifier {output.classifier}
        """


rule predict_hitac_uncertainty:
    input:
        query = "data/test/{dataset}.fasta",
        classifier = "results/temp/{dataset}/hitac_uncertainty/{calibration_method}/{calibration_percentage}/classifier.pkl"
    output:
        predictions = "results/temp/{dataset}/hitac_uncertainty/{calibration_method}/{calibration_percentage}/predictions.pkl"
    benchmark:
        repeat("results/benchmark/{dataset}/predict/{calibration_method}/{calibration_percentage}/hitac_uncertainty.tsv",config["benchmark"]["repeat"])
    threads:
        config["threads"]
    conda:
        "../envs/hitac_uncertainty.yml"
    shell:
        """
        hitac-classify \
            --reads {input.query} \
            --classifier {input.classifier} \
            --kmer 6 \
            --threads {threads} \
            --classification {output.predictions}
        """


rule probability_hitac_uncertainty:
    input:
        query = "data/test/{dataset}.fasta",
        classifier = "results/temp/{dataset}/hitac_uncertainty/{calibration_method}/{calibration_percentage}/classifier.pkl"
    output:
        probabilities = "results/temp/{dataset}/hitac_uncertainty/{calibration_method}/{calibration_percentage}/probabilities.pkl"
    benchmark:
        repeat("results/benchmark/{dataset}/predict/{calibration_method}/{calibration_percentage}/hitac_uncertainty.tsv",config["benchmark"]["repeat"])
    threads:
        config["threads"]
    conda:
        "../envs/hitac_uncertainty.yml"
    shell:
        """
        hitac-probability \
            --reads {input.query} \
            --classifier {input.classifier} \
            --kmer 6 \
            --threads {threads} \
            --probabilities {output.probabilities}
        """


rule filter_hitac_uncertainty:
    input:
        query = "data/test/{dataset}.fasta",
        classifier = "results/temp/{dataset}/hitac_uncertainty/{calibration_method}/{calibration_percentage}/classifier.pkl",
        predictions = "results/temp/{dataset}/hitac_uncertainty/{calibration_method}/{calibration_percentage}/predictions.pkl",
        probabilities = "results/temp/{dataset}/hitac_uncertainty/{calibration_method}/{calibration_percentage}/probabilities.pkl"
    output:
        filtered_sequences = "results/predictions/{dataset}/{calibration_method}/{calibration_percentage}/hitac_uncertainty.tsv"
    benchmark:
        repeat("results/benchmark/{dataset}/predict/{calibration_method}/{calibration_percentage}/hitac_uncertainty_filtered.tsv",config["benchmark"]["repeat"])
    threads:
        config["threads"]
    conda:
        "../envs/hitac_uncertainty.yml"
    shell:
        """
        hitac-filter \
            --classifier {input.classifier} \
            --classification {input.predictions} \
            --probabilities {input.probabilities} \
            --reads {input.query} \
            --threshold 0 \
            --filtered-sequences {output.filtered_sequences}
        """