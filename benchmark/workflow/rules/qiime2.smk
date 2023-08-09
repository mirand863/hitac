rule taxxi_to_qiime2:
    input:
        train = "data/train/{dataset}.fasta",
        scripts = expand("scripts/{script}",script=config["scripts"])
    output:
        reference_reads = temp("results/temp/{dataset}/qiime2/reference_reads.fasta"),
        reference_taxonomy = temp("results/temp/{dataset}/qiime2/reference_taxonomy.txt")
    container:
        config["containers"]["python2"]
    shell:
        """
        python scripts/fasta_utax2qiime.py \
            {input.train} \
            {output.reference_reads} \
            {output.reference_taxonomy}
        """


rule import_qiime2:
    input:
        test = "data/test/{dataset}.fasta",
        reference_reads = "results/temp/{dataset}/qiime2/reference_reads.fasta",
        reference_taxonomy = "results/temp/{dataset}/qiime2/reference_taxonomy.txt"
    output:
        query_reads = temp("results/temp/{dataset}/qiime2/query_reads.qza"),
        reference_reads = temp("results/temp/{dataset}/qiime2/reference_reads.qza"),
        reference_taxonomy = temp("results/temp/{dataset}/qiime2/reference_taxonomy.qza")
    container:
        config["containers"]["qiime2"]
    shell:
        """
        qiime tools import \
            --input-path {input.test} \
            --output-path {output.query_reads} \
            --type 'FeatureData[Sequence]'

        qiime tools import \
            --input-path {input.reference_reads} \
            --output-path {output.reference_reads} \
            --type 'FeatureData[Sequence]'

        qiime tools import \
            --type 'FeatureData[Taxonomy]' \
            --input-format HeaderlessTSVTaxonomyFormat \
            --input-path {input.reference_taxonomy} \
            --output-path {output.reference_taxonomy}
        """


rule export_qiime2:
    input:
        predictions = "results/temp/{dataset}/{method}/predictions.qza"
    output:
        taxonomy = temp("results/temp/{dataset}/{method}/taxonomy.tsv")
    params:
        output_dir = "results/temp/{dataset}/{method}"
    container:
        config["containers"]["qiime2"]
    shell:
        """
        qiime tools export \
            --input-path {input.predictions} \
            --output-path {params.output_dir}
        """


rule qiime2_to_taxxi:
    input:
        taxonomy = "results/temp/{dataset}/{method}/taxonomy.tsv"
    output:
        predictions = "results/predictions/{dataset}/{method}.tsv"
    container:
        config["containers"]["python2"]
    shell:
        """
        python scripts/qiime2tax2tab.py \
            {input.taxonomy} \
            > {output.predictions}
        """
