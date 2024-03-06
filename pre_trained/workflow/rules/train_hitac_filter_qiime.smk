def get_mem_gb(wildcards, attempt):
    return attempt * config["slurm"]["memory_increments_gb"]


rule train_hitac_filter_qiime:
    input:
        reference = "results/imported_qiime2/unite/{dataset}/developer/sh_refs_qiime_{filename}.qza",
        taxonomy = "results/imported_qiime2/unite/{dataset}/developer/sh_taxonomy_qiime_{filename}.qza"
    output:
        classifier = "results/hitac_filter_qiime/unite/{dataset}/developer/sh_refs_qiime_{filename}.qza"
    resources:
        mem_gb = get_mem_gb,
        cpus = 12,
        time = '5-00:00:00'
    threads: 12
    log:
       out = "results/hitac_filter_qiime/unite/{dataset}/developer/sh_refs_qiime_{filename}.out",
       err = "results/hitac_filter_qiime/unite/{dataset}/developer/sh_refs_qiime_{filename}.err"
    conda:
        "../envs/qiime2_2023.2.yml"
    shell:
        """
        qiime hitac fit-filter \
            --i-reference-reads {input.reference} \
            --i-reference-taxonomy {input.taxonomy} \
            --p-kmer 6 \
            --p-threads {resources.cpus} \
            --o-filter {output.classifier} \
            --verbose \
            1> {log.out} \
            2> {log.err}
        """
