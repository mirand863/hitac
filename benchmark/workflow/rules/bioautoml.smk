def get_mem_gb(wildcards, attempt):
    return attempt * 1


rule bioautoml:
    input:
        bioautoml = "results/BioAutoML/BioAutoML-feature.py",
        data = "data/{train_or_test}/{dataset}.fasta"
    output:
        dnc = "results/hitac/features/{train_or_test}/{dataset}/feat_extraction/DNC.csv"
    params:
        bioautoml = "results/BioAutoML",
        dataset = "{dataset}",
        output = "results/hitac/features/{train_or_test}/{dataset}"
    threads:
        config["threads"]
    resources:
        cpus = config["threads"],
        mem_gb = get_mem_gb
    conda:
        "../environments/bioautoml.yml"
    shell:
        """
        cd {params.bioautoml}

        python \
        BioAutoML-feature.py \
        -fasta_train ../../{input.data} \
        -fasta_label_train {params.dataset} \
        -n_cpu {threads} \
        -output ../../{params.output}
        """
