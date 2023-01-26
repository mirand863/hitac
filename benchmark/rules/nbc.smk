rule nbc:
    input:
        train = "data/train/{dataset}.fasta",
        test = "data/test/{dataset}.fasta",
        usearch = "bin/usearch",
        scripts = expand("scripts/{script}", script=config["scripts"])
    output:
        nbc50 = "results/predictions/{dataset}/nbc50.tsv",
        nbc80 = "results/predictions/{dataset}/nbc80.tsv",
        tmpdir = temp(directory("results/temp/{dataset}/nbc"))
    benchmark:
        repeat("results/benchmark/{dataset}/nbc.tsv", config["benchmark"]["repeat"])
    threads:
        config["threads"]
    conda:
        "../envs/nbc.yml"
    shell:
        """
        mkdir -p {output.tmpdir}

        {input.usearch} \
            -nbc_tax \
            {input.test} \
            -db {input.train} \
            -strand plus \
            -tabbedout {output.tmpdir}/raw

        python scripts/bbc_cutoff.py \
            {output.tmpdir}/raw \
            0.5 \
            > {output.nbc50}

        python scripts/bbc_cutoff.py \
            {output.tmpdir}/raw \
            0.8 \
            > {output.nbc80}
        """
