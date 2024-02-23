rule ml_table:
    output:
        table = "results/figures_and_tables/ml_metrics/{dataset}/{rank}.csv"
    params:
        ml_metrics = "results/ml_metrics",
        dataset = "{dataset}",
        rank = "{rank}"
    container:
        config["containers"]["pandas"]
    shell:
        """
        python figures_and_tables/scripts/create_ml_table.py \
            --ml-metrics {params.ml_metrics} \
            --dataset {params.dataset} \
            --rank {params.rank} \
            --output {output.table}
        """
