rule mcr_barplot:
    output:
        plot = "results/figures_and_tables/taxxi_metrics/mcr.pdf"
    params:
        taxxi_metrics = "results/taxxi_metrics",
        datasets = expand("{dataset}", dataset=config["datasets"])
    container:
        config["containers"]["seaborn"]
    shell:
        """
        python figures_and_tables/scripts/plot_mcr.py \
            --taxxi-metrics {params.taxxi_metrics} \
            --datasets {params.datasets} \
            --output {output.plot}
        """
