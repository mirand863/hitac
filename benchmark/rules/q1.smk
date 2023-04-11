rule taxxi_to_qiime1:
    input:
        train = "data/train/{dataset}.fasta",
        scripts = expand("scripts/{script}",script=config["scripts"])
    output:
        reference_reads = temp("results/temp/{dataset}/q1/reference_reads.fasta"),
        reference_taxonomy = temp("results/temp/{dataset}/q1/reference_taxonomy.txt")
    container:
        config["containers"]["python2"]
    shell:
        """
        python scripts/fasta_utax2qiime.py \
            {input.train} \
            {output.reference_reads} \
            {output.reference_taxonomy}
        """


rule q1:
    input:
        test = "data/test/{dataset}.fasta",
        reference_reads = "results/temp/{dataset}/q1/reference_reads.fasta",
        reference_taxonomy = "results/temp/{dataset}/q1/reference_taxonomy.txt"
    output:
        predictions = temp("results/temp/{dataset}/q1/{dataset}_tax_assignments.txt"),
        log = temp("results/temp/{dataset}/q1/{dataset}_tax_assignments.log")
    params:
        tmpdir = "results/temp/{dataset}/q1"
    benchmark:
        repeat("results/benchmark/{dataset}/q1.tsv",config["benchmark"]["repeat"])
    threads:
        config["threads"]
    container:
        config["containers"]["qiime1"]
    shell:
        """
        assign_taxonomy.py \
            -i {input.test} \
            -m uclust \
            -r {input.reference_reads} \
            -t {input.reference_taxonomy} \
            -o {params.tmpdir}
        """


rule qiime1_to_taxxi:
    input:
        predictions = "results/temp/{dataset}/q1/{dataset}_tax_assignments.txt",
        scripts = expand("scripts/{script}", script=config["scripts"])
    output:
        predictions = "results/predictions/{dataset}/q1.tsv"
    container:
        config["containers"]["python2"]
    shell:
        """
        python scripts/qiimetax2tab.py \
            {input.predictions} \
            > {output.predictions}
        """
