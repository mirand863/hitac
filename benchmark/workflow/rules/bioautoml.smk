rule bioautoml:
    input:
        data = "data/{train_or_test}/{dataset}.fasta"
    output:
        dnc = "results/hitac/features/{train_or_test}/{dataset}/feat_extraction/DNC.csv"
    params:
        bioautoml = "/BioAutoML",
        dataset = "{dataset}",
        output = "results/hitac/features/{train_or_test}/{dataset}"
    threads:
        config["threads"]
    container:
        config["containers"]["bioautoml"]
    shell:
        """
        cp -r /BioAutoML/* .

        python BioAutoML-feature.py \
        -fasta_train {input.data} \
        -fasta_label_train {params.dataset} \
        -output {params.output}
        """
