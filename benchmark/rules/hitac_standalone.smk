rule hitac_standalone:
    input:
        reference = "data/train/{dataset}.fasta"
    output:
        classifier = "results/temp/{dataset}/hitac_standalone/classifier.pkl"
    benchmark:
        repeat("results/benchmark/{dataset}/hitac.tsv",config["benchmark"]["repeat"])
    threads:
        config["threads"]
    container:
        config["containers"]["hitac_standalone"]
    shell:
        """
        hitac-fit \
            --reference {input.reference} \
            --kmer 6 \
            --cpus {threads} \
            --classifier {output.classifier}
        """
