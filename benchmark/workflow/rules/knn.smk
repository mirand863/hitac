rule taxxi2knn:
    input:
        train = "data/train/{dataset}.fasta",
        test = "data/test/{dataset}.fasta",
        scripts = expand("scripts/{script}", script=config["scripts"])
    output:
        reference_reads = temp("results/temp/{dataset}/knn/reference_reads.fasta"),
        reference_taxonomy = temp("results/temp/{dataset}/knn/reference_taxonomy.txt"),
        query_reads = temp("results/temp/{dataset}/knn/query_reads.fasta"),
    threads:
        config["threads"]
    container:
        config["containers"]["python2"]
    shell:
        """
        cp {input.test} {output.query_reads}

        python2 scripts/mothur_make_taxtrainfiles.py \
            {input.train} \
            {output.reference_reads} \
            {output.reference_taxonomy}
        """


rule knn:
    input:
        reference_reads = "results/temp/{dataset}/knn/reference_reads.fasta",
        reference_taxonomy = "results/temp/{dataset}/knn/reference_taxonomy.txt",
        query_reads = "results/temp/{dataset}/knn/query_reads.fasta",
    output:
        predictions = temp("results/temp/{dataset}/knn/query_reads.reference_taxonomy.knn.taxonomy"),
        summary = temp("results/temp/{dataset}/knn/query_reads.reference_taxonomy.knn.tax.summary"),
        kmer = temp("results/temp/{dataset}/knn/reference_reads.8mer"),
        tree = temp("results/temp/{dataset}/knn/reference_taxonomy.tree.sum")
    benchmark:
        repeat("results/benchmark/{dataset}/knn.tsv", config["benchmark"]["repeat"])
    threads:
        config["threads"]
    container:
        config["containers"]["knn"]
    shell:
        """
        mothur \
            "#classify.seqs(fasta={input.query_reads}, \
            template={input.reference_reads}, \
            taxonomy={input.reference_taxonomy}, \
            method=knn, processors={threads})"

        rm mothur.*.logfile
        """


rule knn2taxxi:
    input:
        predictions = "results/temp/{dataset}/knn/query_reads.reference_taxonomy.knn.taxonomy",
        scripts = expand("scripts/{script}", script=config["scripts"])
    output:
        predictions = "results/predictions/{dataset}/knn.tsv"
    container:
        config["containers"]["python2"]
    shell:
        """
        python scripts/motknn2utax2.py \
            {input.predictions} \
            > {output.predictions}
        """
