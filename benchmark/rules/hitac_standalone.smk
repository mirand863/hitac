rule hitac_standalone:
    input:
        reference = "data/train/{dataset}.fasta",
        query = "data/test/{dataset}.fasta"
    output:
        classifier = temp("results/temp/{dataset}/hitac_standalone/classifier.pkl"),
        predictions = temp("results/predictions/{dataset}/hitac_standalone.tsv")
    benchmark:
        repeat("results/benchmark/{dataset}/hitac_standalone.tsv",config["benchmark"]["repeat"])
    threads:
        config["threads"]
    container:
        config["containers"]["hitac_standalone"]
    shell:
        """
        hitac-fit \
            --reference {input.reference} \
            --kmer 6 \
            --threads {threads} \
            --classifier {output.classifier}

        hitac-classify \
            --reads {input.query} \
            --classifier {output.classifier} \
            --kmer 6 \
            --threads {threads} \
            --classification {output.predictions}
        """
