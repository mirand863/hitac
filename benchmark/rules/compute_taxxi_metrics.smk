rule compute_taxxi_metrics:
    input:
        scripts = expand("scripts/{script}",script=config["scripts"]),
        namecounts = expand("namecounts/{dataset}",dataset=config["datasets"]),
        predictions = "results/predictions/{dataset}/{penalty}/{solver}/{method}.tsv"
    output:
        metrics = "results/taxxi_metrics/{method}/{dataset}/{penalty}/{solver}/{rank}.tsv"
    container:
        config["containers"]["python2"]
    shell:
        """
        python scripts/taxbenchx.py \
            {wildcards.dataset} \
            {wildcards.method} \
            {wildcards.rank} \
            > {output.metrics}
        """
