rule compute_taxxi_metrics:
    input:
        scripts = expand("scripts/{script}",script=config["scripts"]),
        namecounts = expand("namecounts/{dataset}",dataset=config["datasets"]),
        predictions = "results/predictions/{dataset}/{calibration_method}/{calibration_percentage}/{method}.tsv"
    output:
        metrics = "results/taxxi_metrics/{dataset}/{calibration_method}/{calibration_percentage}/{method}/{rank}.tsv"
    container:
        config["containers"]["python2"]
    shell:
        """
        python scripts/taxbenchx.py \
            {wildcards.dataset} \
            {wildcards.calibration_method}/{wildcards.calibration_percentage}/{wildcards.method} \
            {wildcards.rank} \
            > {output.metrics}
        """
