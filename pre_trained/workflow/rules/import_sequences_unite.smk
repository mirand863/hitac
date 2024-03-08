rule import_sequences_unite:
    input:
        fasta = "results/fix_formatting/unite/{dataset}/developer/sh_refs_qiime_{filename}.fasta"
    output:
        qza = "results/imported_qiime2/unite/{dataset}/developer/sh_refs_qiime_{filename}.qza"
    conda:
        "../envs/qiime2_2023.2.yml"
    shell:
        """
        qiime tools import \
            --type FeatureData[Sequence] \
            --input-path {input.fasta} \
            --output-path {output.qza}
        """
