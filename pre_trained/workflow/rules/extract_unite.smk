checkpoint extract_unite:
    input:
        tar = "data/unite/{dataset}.tgz"
    output:
        dataset = directory("results/data/unite/{dataset}")
    shell:
        """
        mkdir {output.dataset}
        tar -xvzf {input.tar} -C {output.dataset}
        """
