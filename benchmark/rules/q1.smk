rule q1:
    input:
        train = "data/train/{dataset}.fasta",
        test = "data/test/{dataset}.fasta",
        scripts = expand("scripts/{script}", script=config["scripts"])
    output:
        predictions="results/predictions/{dataset}/q1.tsv",
        tmpdir = temp(directory("results/temp/{dataset}/q1"))
    benchmark:
        repeat("results/benchmark/{dataset}/q1.tsv", config["benchmark"]["repeat"])
    threads:
        config["threads"]
    conda:
        "../envs/q1.yml"
    shell:
        """
        mkdir -p {output.tmpdir}

        python scripts/fasta_utax2qiime.py \
            {input.train} \
            {output.tmpdir}/db.fa \
            {output.tmpdir}/tax.txt

        assign_taxonomy.py \
            -i {input.test} \
            -m uclust \
            -r {output.tmpdir}/db.fa \
            -t {output.tmpdir}/tax.txt \
            -o {output.tmpdir}

        python scripts/qiimetax2tab.py \
            {output.tmpdir}/*assignments.txt \
            > {output.predictions}
        """
