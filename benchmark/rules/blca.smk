rule blca:
    input:
        train = "data/train/{dataset}.fasta",
        test = "data/test/{dataset}.fasta",
        blca = "bin/BLCA-2.3-alpha/2.blca_main.py",
        scripts = expand("scripts/{script}", script=config["scripts"])
    output:
        predictions = "results/predictions/{dataset}/blca.tsv",
        tmpdir= temp(directory("results/temp/{dataset}/blca"))
    benchmark:
        repeat("results/benchmark/{dataset}/blca.tsv", config["benchmark"]["repeat"])
    threads:
        config["threads"]
    conda:
        "../envs/blca.yml"
    shell:
        """
        mkdir -p {output.tmpdir}

        python scripts/fasta_utax2_to_blca.py \
            {input.train} \
            {output.tmpdir}/db.fa \
            {output.tmpdir}/tax.txt

        makeblastdb \
            -in {output.tmpdir}/db.fa \
            -dbtype nucl \
            -parse_seqids \
            -out {output.tmpdir}/db

        python scripts/fasta_utax2_to_blca.py \
            {input.test} \
            {output.tmpdir}/q.fa \
            {output.tmpdir}/qtax.txt

        python {input.blca} \
            -i {output.tmpdir}/q.fa \
            -r {output.tmpdir}/tax.txt \
            -q {output.tmpdir}/db \
            --proc {threads}

        python scripts/blca2tab.py \
            {output.tmpdir}/q.fa.blca.out \
            {input.test} \
            > {output.predictions}
        """
