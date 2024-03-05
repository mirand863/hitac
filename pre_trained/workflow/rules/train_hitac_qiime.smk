def get_mem_gb(wildcards, attempt):
    return attempt * config["slurm"]["memory_increments_gb"]


rule train_hitac_qiime:
    input:
        reference = "results/imported_qiime2/unite/{dataset}/developer/sh_refs_qiime_{filename}.qza",
        taxonomy = "results/imported_qiime2/unite/{dataset}/developer/sh_taxonomy_qiime_{filename}.qza"
    output:
        classifier = "results/hitac_qiime/unite/{dataset}/developer/sh_refs_qiime_{filename}.qza"
    resources:
        mem_gb = get_mem_gb,
        cpus = 12,
        time = '5-00:00:00'
    conda:
        "../envs/qiime2_2023.2.yml"
    shell:
        """
        qiime hitac fit \
            --i-reference-reads {input.reference} \
            --i-reference-taxonomy {input.taxonomy} \
            --p-kmer 6 \
            --p-threads {resources.cpus} \
            --o-classifier {output.classifier} \
            --verbose
        """
