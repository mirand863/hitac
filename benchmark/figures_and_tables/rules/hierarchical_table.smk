rule hierarchical_table:
    output:
        table = "results/figures_and_tables/hierarchical_metrics/{dataset}.txt"
    params:
        hierarchical_metrics = "results/hierarchical_metrics",
        dataset = "{dataset}"
    container:
        config["containers"]["pandas"]
    shell:
        """
        python figures_and_tables/scripts/create_hierarchical_table.py \
            --hierarchical-metrics {params.hierarchical_metrics} \
            --dataset {params.dataset} \
            --output {output.table}
        """
