rule hitac_standalone_fit:
    input:
        reference = "data/train/{dataset}.fasta"
    output:
        classifier = temp("results/temp/{dataset}/hitac_standalone/classifier.pkl")
    benchmark:
        repeat("results/benchmark/{dataset}/hitac_standalone_fit.tsv",config["benchmark"]["repeat"])
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
        """


rule hitac_standalone_classify:
    input:
        query = "data/test/{dataset}.fasta",
        classifier = "results/temp/{dataset}/hitac_standalone/classifier.pkl"
    output:
        predictions = "results/predictions/{dataset}/hitac_standalone.tsv"
    benchmark:
        repeat("results/benchmark/{dataset}/hitac_standalone_classify.tsv",config["benchmark"]["repeat"])
    threads:
        config["threads"]
    container:
        config["containers"]["hitac_standalone"]
    shell:
        """
        hitac-classify \
            --reads {input.query} \
            --classifier {input.classifier} \
            --kmer 6 \
            --threads {threads} \
            --classification {output.predictions}
        """
