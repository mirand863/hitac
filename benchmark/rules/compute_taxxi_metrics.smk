rule compute_taxxi_metrics:
    input:
        scripts = expand("scripts/{script}",script=config["scripts"]),
        namecounts = expand("namecounts/{dataset}",dataset=config["datasets"]),
        predictions = "results/predictions/{dataset}/{penalty}/{method}.tsv"
    output:
        metrics = "results/taxxi_metrics/{method}/{dataset}/{penalty}/{rank}.tsv"
    container:
        config["containers"]["python2"]
    shell:
        """
        python scripts/taxbenchx.py \
            {wildcards.dataset} \
            {wildcards.penalty}/{wildcards.method} \
            {wildcards.rank} \
            > {output.metrics}
        """
