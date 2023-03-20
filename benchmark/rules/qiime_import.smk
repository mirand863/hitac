rule qiime_import:
    input:
        test = "data/test/{dataset}.fasta",
        reference_reads = "results/temp/{dataset}/utax2qiime/reference_reads.fasta",
        reference_taxonomy = "results/temp/{dataset}/utax2qiime/reference_taxonomy.txt"
    output:
        query_reads = temp("results/temp/{dataset}/qiime_import/query_reads.qza"),
        reference_reads = temp("results/temp/{dataset}/qiime_import/reference_reads.qza"),
        reference_taxonomy = temp("results/temp/{dataset}/qiime_import/reference_taxonomy.qza")
    container:
        "docker://quay.io/qiime2/core:2023.2"
    shell:
        """
        # export LC_ALL=C.UTF-8
        # export LANG=C.UTF-8

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
