# import os
# import pickle
# from os.path import exists
#
#
# def get_mem_kb(wildcards, attempt):
#     path = f"results/hitac_filter_qiime/unite/{wildcards.dataset}/developer/sh_refs_qiime_{wildcards.filename}_tmpdir"
#     os.makedirs(path,exist_ok=True)
#     filename = f"{path}/allocated_memory.sav"
#     allocated_memory = attempt * config["slurm"]["memory_increments_kb"]
#     if exists(filename):
#         (_, stored_attempt) = pickle.load(open(filename,"rb"))
#         attempt = max(stored_attempt + 1, attempt)
#         allocated_memory = attempt * config["slurm"]["memory_increments_kb"]
#     with open(filename,"wb") as file:
#         pickle.dump(("attempt", attempt),file)
#     return allocated_memory

def get_mem_kb(wildcards, attempt):
    return attempt * config["slurm"]["memory_increments_kb"]


rule train_hitac_filter_qiime:
    input:
        reference = "results/imported_qiime2/unite/{dataset}/developer/sh_refs_qiime_{filename}.qza",
        taxonomy = "results/imported_qiime2/unite/{dataset}/developer/sh_taxonomy_qiime_{filename}.qza"
    output:
        classifier = "results/hitac_filter_qiime/unite/{dataset}/developer/sh_refs_qiime_{filename}.qza",
        md5 = "results/hitac_filter_qiime/unite/{dataset}/developer/sh_refs_qiime_{filename}.md5"
    params:
        tmp_dir = "results/hitac_filter_qiime/unite/{dataset}/developer/sh_refs_qiime_{filename}_tmpdir"
    resources:
        mem_kb = get_mem_kb,
        cpus = 1,
        time = '5-00:00:00'
    threads: 1
    benchmark:
        "results/hitac_filter_qiime/unite/{dataset}/developer/sh_refs_qiime_{filename}.tsv"
    conda:
        "../envs/qiime2_2023.2.yml"
    shell:
        """
        export PYTHONUNBUFFERED=1

        ulimit -m {resources.mem_kb}
        ulimit -v {resources.mem_kb}

        mkdir -p {params.tmp_dir}

        qiime hitac fit-filter \
            --i-reference-reads {input.reference} \
            --i-reference-taxonomy {input.taxonomy} \
            --p-kmer 6 \
            --p-threads {resources.cpus} \
            --p-tmp-dir {params.tmp_dir} \
            --o-filter {output.classifier} \
            --verbose

        md5sum {output.classifier} \
            > {output.md5}

        rm -rf {params.tmp_dir}
        """
