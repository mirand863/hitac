rule taxxi_table:
    output:
        table = "results/figures_and_tables/taxxi_metrics/{dataset}/{rank}.txt"
    params:
        taxxi_metrics = "results/taxxi_metrics",
        dataset = "{dataset}",
        rank = "{rank}"
    container:
        config["containers"]["pandas"]
    shell:
        """
        python figures_and_tables/scripts/create_taxxi_table.py \
            --taxxi-metrics {params.taxxi_metrics} \
            --dataset {params.dataset} \
            --rank {params.rank} \
            --output {output.table}
        """
