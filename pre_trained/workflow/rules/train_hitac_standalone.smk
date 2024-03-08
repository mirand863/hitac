def get_mem_gb(wildcards, attempt):
    return attempt * config["slurm"]["memory_increments_gb"]


rule train_hitac_standalone:
    input:
        reference = "results/converted_taxxi/unite/{dataset}/developer/sh_refs_qiime_{filename}.fasta"
    output:
        classifier = "results/hitac_standalone/unite/{dataset}/developer/sh_refs_qiime_{filename}.pkl"
    params:
        tmp_dir = "results/hitac_standalone/unite/{dataset}/developer/sh_refs_qiime_{filename}_tmpdir"
    resources:
        mem_gb = get_mem_gb,
        cpus = 1,
        time = '5-00:00:00'
    threads: 1
    benchmark:
        "results/hitac_standlone/unite/{dataset}/developer/sh_refs_qiime_{filename}.tsv"
    conda:
        "../envs/hitac.yml"
    shell:
        """
        export PYTHONUNBUFFERED=1

        mkdir -p {params.tmp_dir}

        hitac-fit \
            --reference {input.reference} \
            --kmer 6 \
            --threads {resources.cpus} \
            --classifier {output.classifier}

        rm -rf {params.tmp_dir}
        """