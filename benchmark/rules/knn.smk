rule knn:
    input:
        train = "data/train/{dataset}.fasta",
        test = "data/test/{dataset}.fasta",
        scripts = expand("scripts/{script}", script=config["scripts"])
    output:
        predictions = "results/predictions/{dataset}/knn.tsv",
        tmpdir = temp(directory("results/temp/{dataset}/knn"))
    benchmark:
        repeat("results/benchmark/{dataset}/knn.tsv", config["benchmark"]["repeat"])
    threads:
        config["threads"]
    conda:
        "../envs/knn.yml"
    shell:
        """
        mkdir -p {output.tmpdir}

        cp {input.test} {output.tmpdir}/q.fasta

        python2 scripts/mothur_make_taxtrainfiles.py \
            {input.train} \
            {output.tmpdir}/dbmot.fa \
            {output.tmpdir}/dbtax.txt

        mothur \
            "#classify.seqs(fasta={output.tmpdir}/q.fasta, \
            template={output.tmpdir}/dbmot.fa, \
            taxonomy={output.tmpdir}/dbtax.txt, \
            method=knn, processors={threads})"

        python2 scripts/motknn2utax2.py \
            {output.tmpdir}/q.dbtax.knn.taxonomy \
            > {output.predictions}

        rm -rf mothur.*
        """
