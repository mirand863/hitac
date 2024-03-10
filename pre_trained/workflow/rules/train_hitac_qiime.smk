def get_mem_kb(wildcards, attempt):
    return attempt * config["slurm"]["memory_increments_kb"]


rule train_hitac_qiime:
    input:
        reference = "results/imported_qiime2/unite/{dataset}/developer/sh_refs_qiime_{filename}.qza",
        taxonomy = "results/imported_qiime2/unite/{dataset}/developer/sh_taxonomy_qiime_{filename}.qza"
    output:
        classifier = "results/hitac_qiime/unite/{dataset}/developer/sh_refs_qiime_{filename}.qza"
    params:
        tmp_dir = "results/hitac_qiime/unite/{dataset}/developer/sh_refs_qiime_{filename}_tmpdir"
    resources:
        mem_kb = get_mem_kb,
        cpus = 1,
        time = '5-00:00:00'
    threads: 1
    benchmark:
        "results/hitac_qiime/unite/{dataset}/developer/sh_refs_qiime_{filename}.tsv"
    conda:
        "../envs/qiime2_2023.2.yml"
    shell:
        """
        export PYTHONUNBUFFERED=1

        ulimit -m 1000000

        mkdir -p {params.tmp_dir}

        qiime hitac fit \
            --i-reference-reads {input.reference} \
            --i-reference-taxonomy {input.taxonomy} \
            --p-kmer 6 \
            --p-threads {resources.cpus} \
            --p-tmp-dir {params.tmp_dir} \
            --o-classifier {output.classifier} \
            --verbose

        rm -rf {params.tmp_dir}
        """
