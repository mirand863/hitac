rule compute_metrics:
    input:
        scripts = expand("scripts/{script}",script=config["scripts"]),
        namecounts = expand("namecounts/{dataset}",dataset=config["datasets"])
    output:
        metrics = "results/metrics/{method}/{dataset}/{rank}.tsv"
    container:
        "docker://python:2.7-slim"
    shell:
        """
        python scripts/taxbenchx.py \
            {wildcards.dataset} \
            {wildcards.method} \
            {wildcards.rank} \
            > {output.metrics}
        """
