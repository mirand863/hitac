checkpoint extract_unite:
    input:
        tar = "data/unite/{dataset}.tgz"
    output:
        touch("results/data/unite/{dataset}.done")
    params:
        output_folder = directory("results/data/unite/{dataset}")
    shell:
        """
        mkdir -p {params.output_folder}
        tar -xvzf {input.tar} -C {params.output_folder}
        """
