rule compute_ml_metrics_for_rank:
    input:
        scripts = expand("scripts/{script}",script=config["scripts"]),
        predictions = "results/predictions/{dataset}/{method}.tsv"
    output:
        metrics = "results/ml_metrics/{method}/{dataset}/{rank}.tsv"
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
