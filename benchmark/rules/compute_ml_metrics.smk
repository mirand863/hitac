rule compute_ml_metrics:
    input:
        scripts = expand("scripts/{script}",script=config["scripts"]),
        predictions = "results/predictions/{dataset}/{penalty}/{method}.tsv"
    output:
        metrics = "results/ml_metrics/{method}/{dataset}/{penalty}/{rank}.tsv"
    container:
        config["containers"]["metrics"]
    shell:
        """
        python scripts/compute_ml_metrics.py \
            --predictions {input.predictions} \
            --dataset {wildcards.dataset} \
            --method {wildcards.method} \
            --rank {wildcards.rank} \
            --metrics {output.metrics}
        """
