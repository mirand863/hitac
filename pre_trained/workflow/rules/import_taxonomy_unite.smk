rule import_taxonomy_unite:
    input:
        taxonomy = "results/data/unite/{dataset}/developer/sh_taxonomy_qiime_{filename}.txt"
    output:
        qza = "results/imported_qiime2/unite/{dataset}/developer/sh_taxonomy_qiime_{filename}.qza"
    conda:
        "../envs/qiime2_2023.2.yml"
    shell:
        """
        qiime tools import \
            --type FeatureData[Taxonomy] \
            --input-path {input.taxonomy} \
            --output-path {output.qza}
        """
