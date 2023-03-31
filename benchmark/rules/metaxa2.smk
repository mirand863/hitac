rule taxxi_to_metaxa2:
    input:
        train = "data/train/{dataset}.fasta",
        scripts = expand("scripts/{script}",script=config["scripts"])
    output:
        reference_reads = temp("results/temp/{dataset}/metaxa2/reference_reads.fasta"),
        reference_taxonomy = temp("results/temp/{dataset}/metaxa2/reference_taxonomy.txt"),
    container:
        config["containers"]["python2"]
    shell:
        """
        python scripts/fasta_utax2_to_metaxa2.py \
            {input.train} \
            {output.reference_reads} \
            {output.reference_taxonomy}
        """


rule metaxa2:
    input:
        train = "data/train/{dataset}.fasta",
        test = "data/test/{dataset}.fasta",
        scripts = expand("scripts/{script}",script=config["scripts"])
    output:
        predictions="results/predictions/{dataset}/metaxa2.tsv",
        tmpdir = temp(directory("results/temp/{dataset}/metaxa2"))
    benchmark:
        repeat("results/benchmark/{dataset}/metaxa2.tsv", config["benchmark"]["repeat"])
    threads:
        config["threads"]
    conda:
        '../envs/metaxa2.yml'
    shell:
        """
        mkdir -p {output.tmpdir}
        
        python scripts/fasta_utax2_to_metaxa2.py \
            {input.train} \
            {output.tmpdir}/db.fa \
            {output.tmpdir}/tax.txt

        metaxa2_dbb \
            -b {output.tmpdir}/db.fa \
            -o {output.tmpdir}/outdb \
            -t {output.tmpdir}/tax.txt \
            --auto_rep T \
            --cpu {threads} \
            --mode divergent
        
        metaxa2 \
            -i {input.test} \
            -d {output.tmpdir}/outdb/blast \
            -p {output.tmpdir}/outdb/HMMs \
            -o {output.tmpdir}/results \
            -cpu {threads}
        
        python scripts/metaxa2tab.py \
            {output.tmpdir}/results.taxonomy.txt \
            {input.test} \
            > {output.predictions}
        """
