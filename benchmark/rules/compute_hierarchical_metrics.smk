rule compute_hierarchical_metrics:
    input:
        scripts = expand("scripts/{script}",script=config["scripts"]),
        predictions = "results/predictions/{dataset}/{method}.tsv"
    output:
        metrics = "results/hierarchical_metrics/{method}/{dataset}.tsv"
    container:
        config["containers"]["hierarchical_metrics"]
    shell:
        """
        python scripts/compute_hierarchical_metrics.py \
            --predictions {input.predictions} \
            --dataset {wildcards.dataset} \
            --method {wildcards.method} \
            --metrics {output.metrics}
        """
