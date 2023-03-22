rule import_qiime2:
    input:
        test = "data/test/{dataset}.fasta",
        reference_reads = "results/temp/{dataset}/taxxi_to_qiime2/reference_reads.fasta",
        reference_taxonomy = "results/temp/{dataset}/taxxi_to_qiime2/reference_taxonomy.txt"
    output:
        query_reads = temp("results/temp/{dataset}/import_qiime2/query_reads.qza"),
        reference_reads = temp("results/temp/{dataset}/import_qiime2/reference_reads.qza"),
        reference_taxonomy = temp("results/temp/{dataset}/import_qiime2/reference_taxonomy.qza")
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
