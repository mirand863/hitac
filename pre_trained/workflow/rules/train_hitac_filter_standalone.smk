def get_mem_kb(wildcards, attempt):
    return attempt * config["slurm"]["memory_increments_kb"]


rule train_hitac_filter_standalone:
    input:
        reference = "results/converted_taxxi/unite/{dataset}/developer/sh_refs_qiime_{filename}.fasta"
    output:
        filter = "results/hitac_filter_standalone/unite/{dataset}/developer/sh_refs_qiime_{filename}.pkl"
    params:
        tmp_dir = "results/hitac_filter_standalone/unite/{dataset}/developer/sh_refs_qiime_{filename}_tmpdir"
    resources:
        mem_kb = get_mem_kb,
        cpus = 1,
        time = '5-00:00:00'
    threads: 1
    benchmark:
        "results/hitac_filter_standlone/unite/{dataset}/developer/sh_refs_qiime_{filename}.tsv"
    conda:
        "../envs/hitac.yml"
    shell:
        """
        export PYTHONUNBUFFERED=1

        ulimit -m 1000000

        mkdir -p {params.tmp_dir}

        hitac-fit-filter \
            --reference {input.reference} \
            --kmer 6 \
            --threads {resources.cpus} \
            --filter {output.filter}

        rm -rf {params.tmp_dir}
        """
