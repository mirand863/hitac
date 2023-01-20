rule microclass:
    input:
        train = "data/train/{dataset}.fasta",
        test = "data/test/{dataset}.fasta",
        scripts = expand("scripts/{script}", script=config["scripts"])
    output:
        predictions="results/predictions/{dataset}/microclass.tsv",
        tmpdir = temp(directory("results/temp/{dataset}/microclass"))
    benchmark:
        repeat("results/benchmark/{dataset}/microclass.tsv", config["benchmark"]["repeat"])
    threads:
        config["threads"]
    conda:
        "../envs/microclass.yml"
    shell:
        """
        mkdir -p {output.tmpdir}

        Rscript scripts/microclass.R \
            {input.train} \
            {input.test} \
            {output.tmpdir}/microclass.tsv

        python scripts/microclass2tab.py \
            {output.tmpdir}/microclass.tsv \
            {output.predictions}
        """
